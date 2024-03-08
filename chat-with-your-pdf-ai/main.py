import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores.faiss import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.chains.question_answering import load_qa_chain
from langchain_openai import OpenAI

# --- UI Configurations --- #
st.set_page_config(page_title="Chat with your PDF File", page_icon=":open_book:")

st.markdown("# :rainbow[Chat with your PDF File] :open_book:")


def process_text(text):
    # Split text into chunks
    text_splitter = CharacterTextSplitter(
        separator="\n", chunk_size=1000, chunk_overlap=50, length_function=len
    )
    chunks = text_splitter.split_text(text)

    # Convert text chunks into embeddings to create vector index
    embeddings = OpenAIEmbeddings()
    vector_index = FAISS.from_texts(chunks, embeddings)

    return vector_index


def main():
    pdf = st.file_uploader("Upload your PDF File", type="pdf")

    if pdf:
        pdf_reader = PdfReader(pdf)

        # Initialize an empty string to store text from PDF
        text = ""

        # Iterate through each page and append the extracted text 
        for page in pdf_reader.pages:
            text += page.extract_text()

        vector_index = process_text(text)

        query = st.text_input("Ask a question to the PDF File")

        if query:
            docs = vector_index.similarity_search(query)
            llm = OpenAI()
            chain = load_qa_chain(llm, chain_type="stuff")
            input_data = {"input_documents": docs, "question": query}
            response = chain.invoke(input=input_data)
            output_text = response.get('output_text')

            # --- print only the sources --- #
            # for i, doc in enumerate(response.get('input_documents', [])):
            #     page_content = doc.page_content if hasattr(doc, 'page_content') else 'No content available'
            #     st.write(f"Source {i + 1}: {page_content}")

            # --- print only the answer--- #
            st.write(output_text)

            # --- print everything --- #
            # st.write(response)


if __name__ == "__main__":
    main()
