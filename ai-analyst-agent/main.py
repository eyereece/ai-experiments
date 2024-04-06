import os
import re

from pathlib import Path
from typing import Optional, Type

from langchain.indexes import VectorstoreIndexCreator
from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools.retriever import create_retriever_tool
from langchain_openai import OpenAIEmbeddings, ChatOpenAI

from langchain_community.document_loaders import CSVLoader
from langchain_community.document_loaders import DataFrameLoader
from langchain_community.vectorstores import FAISS
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field

from langchain_experimental.tools import PythonAstREPLTool
from langchain.prompts import PromptTemplate
from langchain.tools import BaseTool

import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns

from prompts import csv_template, react_template

# --- CONFIGURATIONS --- #
embedding_model = OpenAIEmbeddings()
GPT_MODEL = "gpt-4"
PAGE_CONTENT_COL = "book_name" # change this
CONTENT_COL_SEARCH = "books_review_search" # change this


# --- Helper Functions --- #
def extract_code(response):
    PATTERN = r"(`(python)?(?P<code_block>.*?)`)" 
    code = "\n".join(match.group("code_block").strip() for match in re.finditer(PATTERN, response, re.DOTALL))

    return code


def execute_code(response: str, df: pd.DataFrame):
    code = extract_code(response)

    # if theres code in response, try to execute
    if code:
        try:
            exec(code, globals(), locals())
            if "plt" in locals() and plt.gcf().get_axes():
                # get current figure and display it
                fig = plt.gcf()
                st.pyplot(fig)
            else:
                print("No plot detected")
        except Exception as e:
            st.error(f"{str(e)}")
    else:
        print("No code detected")

def extract_tool_and_input(response):
    try:
        if len(response.get("intermediate_steps", [])) < 1:
            raise ValueError("No intermediate steps found")

        try:
            # Prioritize single-nested tool and tool_input
            tool_data = response["intermediate_steps"][0][0]
            tool = tool_data.tool if hasattr(tool_data, 'tool') else None
            tool_input = tool_data.tool_input if hasattr(tool_data, 'tool_input') else None
        except (IndexError, AttributeError) as e:
            # Fallback to non-nested tool and tool_input
            tool_data = response["intermediate_steps"][0]
            tool = tool_data.tool if hasattr(tool_data, 'tool') else None
            tool_input = tool_data.tool_input if hasattr(tool_data, 'tool_input') else None
            print(f"Handling single-nested structure: {str(e)}")

        if tool is None or tool_input is None:
            # Handle empty tool or tool_input
            st.write(response["output"])
            return None, None

        return tool, tool_input

    except (IndexError, AttributeError, ValueError) as e:
        print(f"Error processing response: {str(e)}")
        return None, None

# --- UI Configuration --- #
st.set_page_config(page_title="LangChain: AI Analyst", page_icon="📊")
st.title("📊 AI Analyst")

openai_api_key = st.sidebar.text_input("openai_api_key", type="password")


# --- Main Page --- #
def main():
    uploaded_file = st.file_uploader("Upload a csv file", type="csv")

    if uploaded_file:
        # load as df
        df = pd.read_csv(uploaded_file)

        # load as vector store
        loader = DataFrameLoader(df, page_content_column=PAGE_CONTENT_COL)
        docs = loader.load()

        index_creator = VectorstoreIndexCreator(vectorstore_cls=FAISS)
        vectorstore = FAISS.from_documents(docs, embedding_model)

        # create retriever tool
        retriever_tool = create_retriever_tool(
            vectorstore.as_retriever(),
            name=CONTENT_COL_SEARCH,
            description="Search for customer reviews",
        )

        # Create REPL tool
        class PythonInputs(BaseModel):
            query: str = Field(description="code snippet to run")

        repl = PythonAstREPLTool(
            locals={"df": df},
            name="python_repl",
            description="Runs code and returns the output of the final line",
            args_schema=PythonInputs,
        )

        # initialize agent tools
        tools = [repl, retriever_tool]

        # Create Prompt to combine react and csv prompt
        instructions = csv_template.format(dhead=df.head().to_markdown(), CONTENT_COL_SEARCH=CONTENT_COL_SEARCH)
        base_prompt = PromptTemplate.from_template(react_template)
        full_prompt = base_prompt.partial(instructions=instructions)

        # Create react agent
        react_agent = create_react_agent(
            llm=ChatOpenAI(temperature=0, model=GPT_MODEL, streaming=True),
            tools=tools,
            prompt=full_prompt,
        )

        agent_executor = AgentExecutor(
            agent=react_agent,
            tools=tools,
            verbose=True,
            return_intermediate_steps=True,
            handle_parsing_errors=True,
        )

        query = st.chat_input("Ask an AI Analyst about your data")

        if query:
            st.chat_message("user").write(query)

            if not openai_api_key:
                st.info("Please add your OpenAI API Key to continue. ")
                st.stop()

            with st.chat_message("assistant"):
                st_callback = StreamlitCallbackHandler(st.container())
                response = agent_executor.invoke(
                    {"input": query}, {"callbacks": [st_callback]}
                )

                tool, tool_input = extract_tool_and_input(response)

                if tool == "python_repl":
                    try:
                        execute_code(tool_input, df)
                    except Exception as e:
                        print(f"Error executing code: {str(e)}")
                
                else:
                    st.write(response["output"])


if __name__ == "__main__":
    main()
