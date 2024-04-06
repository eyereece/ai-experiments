<h2 align="center">AI Analyst Agent with LangChain, GPT-4, and Streamlit</h2>
<br>

<center>
<img src='https://img.shields.io/badge/App-AI_Analyst_Agent-brown' alt='Project Page'>
</center>

Read the blog post here for full explanation:
<a href="https://www.joankusuma.com/post/building-an-ai-analyst-agent-with-langchain-and-llm">Build an AI Analyst Agent with LangChain, GPT-4, and Streamlit</a>

<img src="https://static.wixstatic.com/media/81114d_42cb2cdce1d34edea002bacd6c0b99aa~mv2.png" alt="agent-workflow" height="450" width="800">

<br>

# Features
A web app that utilizes an AI agent that can provide data analysis, create and display plots for you given a query and a dataset.
* <b>In-Context Learning:</b> Combined two prompting methods to guide the model. Particularly, how the agent should  approach a problem given a question and which tool to use given a situation.
* <b>Toolkits:</b> The Agent is equiped with a vector retriever tool and python code runner tool.
* <b>Plot Display and Analysis: </b> Currently, the system has been optimized to handle plot displays, particularly plots from the Matplotlib library. Agent can also analyze queries related to dataset.
  
<br>

# Sample Results

<img src="https://static.wixstatic.com/media/81114d_5bbf39872d054a4bb20fd7a98df37006~mv2.png" alt="demo-1" height="450" width="600">

<img src="https://static.wixstatic.com/media/81114d_96353f7521d14ebaba863c088b4f7be8~mv2.png" alt="demo-1" height="450" width="600">

<br>

# Quick Start 1

The following quickstart uses the provided dataset, you will only need your own OpenAI API Key, you will insert your API Key on the left sidebar after running the app.

Clone the repository
```bash
git clone https://github.com/eyereece/ai-projects.git
```

Navigate to the project directory:
```bash
cd ai-projects/ai-analyst-agent
```

Install dependencies
```bash
pipenv install
```

To use the app with a custom dataset, follow all the steps above and head down to Quick Start 2, and then come back here

(OPTIONAL) Configure UI for Streamlit
This will make the background white when running the app
```bash
mkdir .streamlit
cd .streamlit
touch config.toml
echo "[theme]\nbase=\"light\"\nprimaryColor=\"#6b4bff\"" > config.toml
```


Run the streamlit app:
```bash
streamlit run main.py
```

To use the app with the provided dataset, load the dataset that was cloned along with the rest of the file titled "customer_reviews_1.csv" and ask questions about the data.

<br>

# Quick Start 2

You will need to adjust a few configurations to use the app with your own dataset, make sure you use a clean dataset for best result.

Adjust Configurations in main.py, it should be under the comment line # --- CONFIGURATIONS --- #
* PAGE_CONTENT_COL should be changed the main column name of the dataset. For example, if your dataset is reviews for tv shows, and the column name for the title of the tv shows is tv_show_name, then you should change it to: PAGE_CONTENT_COL = "tv_show_name"
* CONTENT_COL_SEARCH should be changed to the name you want, it is the name of the vector search tool. For example, if the data is about tv shows, you may change it to "tv_show_search", or other descriptive name of your choice.

```bash
# --- CONFIGURATIONS --- #
embedding_model = OpenAIEmbeddings()
GPT_MODEL = "gpt-4"
PAGE_CONTENT_COL = "book_name" # change this
CONTENT_COL_SEARCH = "books_review_search" # change this
```

Adjust prompt in prompts.py for csv_template, particularly the following section:

```bash
You have a tool called {CONTENT_COL_SEARCH} through which you can lookup a book by name and find the records corresponding to reviews with similar name as the query.
You should only really use this if your search term contains a books name. Otherwise, try to solve it with code.
The dataset can be accessed with a variable named 'df'.
Remember to import necessary libraries if needed.

For example:

<question>What is the review for the book How to Catch a Turkey?</question>
<logic>Use {CONTENT_COL_SEARCH} since you can use the query `How to Catch a Turkey`</logic>

<question>Which book name has the highest mean reviewer rating?</question>
<logic>Use `python_repl` since even though the question is about a book, you don't know its name so you can't include it.</logic>
"""
```

For example, let's use our running example of a dataset about tv shows, you can adjust the above prompt to the below:

```bash
You have a tool called {CONTENT_COL_SEARCH} through which you can lookup a tv show by name and find the records corresponding to reviews with similar name as the query.
You should only really use this if your search term contains a tv shows name. Otherwise, try to solve it with code.
The dataset can be accessed with a variable named 'df'.
Remember to import necessary libraries if needed.

For example:

<question>What is the review for the tv show Stranger Things?</question>
<logic>Use {CONTENT_COL_SEARCH} since you can use the query `Stranger Things`</logic>

<question>Which tv show has the highest mean reviewer rating?</question>
<logic>Use `python_repl` since even though the question is about a tv show, you don't know its name so you can't include it.</logic>
"""
```

Run the app as outlined in QuickStart 1

<br>

# References

Prompt has been slightly modified from an existing "hwchase17/react" prompt and "csv-agent" available through these links:
* https://smith.langchain.com/hub/hwchase17/react?organizationId=529179d8-5092-5e66-a0f8-1a11e45e8d25
* https://github.com/langchain-ai/langchain/blob/master/templates/csv-agent/csv_agent/agent.py
