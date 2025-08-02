__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from langchain.chains import create_sql_query_chain
from langchain_community.utilities import SQLDatabase
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_google_genai import GoogleGenerativeAI
from langchain_community.vectorstores import Chroma
from langchain.prompts import PromptTemplate, FewShotPromptTemplate
from langchain.prompts.example_selector import SemanticSimilarityExampleSelector
from langchain_core.tools import Tool
from few_shots import few_shots
from tabulate import tabulate
from dotenv import load_dotenv
from db_connection import get_langchain_db

import pandas as pd
import os

# Load .env and API key
load_dotenv()
api_key = os.getenv("API_KEY")

# Global variable to store the last executed query
_last_sql_query = None

def run_sql_query(query: str, db) -> str:
    global _last_sql_query
    
    # Store the query globally so we can access it later
    _last_sql_query = query
    
    # Remove markdown code block formatting if present
    if query.startswith("```"):
        lines = query.split("\n")
        clean_lines = lines[1:-1] if lines[-1].strip() == "```" else lines[1:]
        query = "\n".join(clean_lines)
    
    try:
        with db._engine.connect() as conn:
            df = pd.read_sql(query, conn)
            if df.empty:
                return "No results found."
            return tabulate(df, headers='keys', tablefmt='grid', showindex=False)
    except Exception as e:
        return f"Query failed: {str(e)}"

def get_last_sql_query():
    """Return the last executed SQL query"""
    return _last_sql_query


# ✅ Main function to build the chain
def get_few_shot_db_chain():
    db = get_langchain_db()
    llm = GoogleGenerativeAI(google_api_key=api_key, model="gemini-2.0-flash", temperature=0.2)
    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')

    # Prepare few-shot examples for similarity search
    to_vectorize = [" ".join(example.values()) for example in few_shots]
    vectorstore = Chroma.from_texts(to_vectorize, embedding=embeddings, metadatas=few_shots)

    example_selector = SemanticSimilarityExampleSelector(
        vectorstore=vectorstore,
        k=2
    )

    # Template for few-shot prompting
    example_prompt = PromptTemplate(
        input_variables=["Question", "SQLQuery", "SQLResult", "Answer"],
        template="\nQuestion: {Question}\nSQLQuery: {SQLQuery}\nSQLResult: {SQLResult}\nAnswer: {Answer}"
    )

    # Prompt that guides the LLM
    mysql_prompt = """You are a MySQL expert. Given an input question, first create a syntactically correct MySQL query to run, then look at the results of the query and return the answer to the input question.
Unless the user specifies in the question a specific number of examples to obtain, query for at most {top_k} results using the LIMIT clause as per MySQL. You can order the results to return the most informative data in the database.
Never query for all columns from a table. You must query only the columns that are needed to answer the question. Wrap each column name in backticks (`) to denote them as delimited identifiers.
Pay attention to use only the column names you can see in the tables below. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.
Pay attention to use CURDATE() function to get the current date, if the question involves "today".

Use the following format:

Question: Question here
SQLQuery: Query to run with no pre-amble
SQLResult: Result of the SQLQuery
Answer: Final answer here

No pre-amble."""

    PROMPT_SUFFIX = "\nOnly use the tables listed below.\n{table_info}\nQuestion: {input}"

    few_shot_prompt = FewShotPromptTemplate(
        example_selector=example_selector,
        example_prompt=example_prompt,
        prefix=mysql_prompt,
        suffix=PROMPT_SUFFIX,
        input_variables=["input", "table_info", "top_k"],
    )

    # Chain to write SQL query using LLM
    write_query = create_sql_query_chain(llm, db, prompt=few_shot_prompt)

    # ✅ Use new Tool wrapper instead of deprecated QuerySQLDatabaseTool
    execute_query = Tool.from_function(
        func=lambda query: run_sql_query(query, db),
        name="SQL Query Executor",
        description="Executes a SQL query on the database and returns results as a table.",
    )

    # Combine generation and execution into one chain
    chain = write_query | execute_query
    return chain
