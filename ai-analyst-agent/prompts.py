csv_template = """You are working with a pandas dataframe in Python. The name of the dataframe is `df`.
It is important to understand the attributes of the dataframe before working with it. This is the result of running `df.head().to_markdown()`

<df>
{dhead}
</df>

You are not meant to use only these rows to answer questions - they are meant as a way of telling you about the shape and schema of the dataframe.
You also do not have to use only the information here to answer questions - you can run intermediate queries to do exporatory data analysis to give you more information as needed.

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

react_template = """

{instructions}

TOOLS:
------
You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}
"""
