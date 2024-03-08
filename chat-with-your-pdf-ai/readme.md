<h2 align="center">Chat with your PDF with LangChain and OpenAI API</h2>
<br>

<center>
<img src='https://img.shields.io/badge/App-Chat_with_your_pdf-blue' alt='Project Page'>
</center>


Read the blog post here for explanation:
<a href="https://www.joankusuma.com/post/build-an-ai-app-to-chat-with-your-pdf-using-langchain-and-openai-api">Chat with your PDF App</a>

# Features
A simple AI Question-Answering App that allows you to ask questions about your PDF file: research papers, resumes, ect

# Sample Results

Sample result with the original RAG research paper <br>
<img src="https://static.wixstatic.com/media/81114d_888260175cd14e9aa8b4f99c1997a0d7~mv2.png" alt="demo-1" height="350" width="600">

<br>

Sample result with an afternoon tea menu <br>
<img src="https://static.wixstatic.com/media/81114d_32d9deb378fb46979a3904ea4ec07b57~mv2.png" alt="demo-2" height="350" width="600">

# Getting Started

Clone the repository, navigate to the project directory and activate virtual environment

Install Dependencies in pipfile:
```bash
pipenv install 
```

Create a .env file and put in your API key:
```bash
OPENAI_API_KEY="insert-your-api-key-here"
```

Run the streamlit app on your CLI:
```bash
streamlit run main.py
```

# Usage
* Upload a pdf file
* insert questions you have about the file and press enter


# PDF Files I used for the demo is available here
* <a href="https://arxiv.org/abs/2005.11401">Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks</a>
* <a href="https://www.fairmont.com/seattle/dining/afternoon-tea/">Afternoon Tea Menu</a>
