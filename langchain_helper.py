from langchain.chains.sql_database.prompt import PROMPT_SUFFIX, _mysql_prompt
from langchain_community.tools.sql_database.tool import QuerySQLDatabaseTool
from langchain.prompts import SemanticSimilarityExampleSelector
from langchain.prompts.prompt import PromptTemplate
from langchain.prompts import FewShotPromptTemplate
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_google_genai import GoogleGenerativeAI 
from langchain.chains import create_sql_query_chain
from langchain.vectorstores import Chroma
from few_shots import few_shots
from dotenv import load_dotenv
import os
from db_connection import get_langchain_db

# Create a custom tool that extends QuerySQLDatabaseTool to clean queries
class CleanQuerySQLDatabaseTool(QuerySQLDatabaseTool):
    def _run(self, query: str, **kwargs):
        # Remove markdown code block formatting if present
        if query.startswith("```"):
            # Extract the query from the markdown code block
            lines = query.split("\n")
            # Remove the first line (```sql) and the last line (```
            clean_lines = lines[1:-1] if lines[-1].strip() == "```" else lines[1:]
            query = "\n".join(clean_lines)
            print ("SQL QUERY:", query)
        return super()._run(query, **kwargs)

load_dotenv()
api_key = os.getenv("API_KEY")

def get_few_shot_db_chain():
    db = get_langchain_db()
    llm = GoogleGenerativeAI(google_api_key=api_key, model = "gemini-2.0-flash", temperature=0.2)
    embeddings = HuggingFaceEmbeddings(model_name = 'sentence-transformers/all-MiniLM-L6-v2')

    to_vectorize = [" ".join(example.values()) for example in few_shots]
    vectorstore = Chroma.from_texts(to_vectorize, embedding = embeddings, metadatas = few_shots)

    example_selector = SemanticSimilarityExampleSelector(
        vectorstore = vectorstore,
        k=2)
    
    example_prompt = PromptTemplate(
        input_variables=["Question", "SQLQuery", "SQLResult", "Answer"],
        template="\nQuestion: {Question}\nSQLQuery: {SQLQuery}\nSQLResult: {SQLResult}\nAnswer: {Answer}"
    )

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
    
    No pre-amble.
    """

    few_shot_prompt = FewShotPromptTemplate(
        example_selector=example_selector,
        example_prompt=example_prompt,
        prefix= mysql_prompt,
        suffix=PROMPT_SUFFIX,
        input_variables = ["input", "table_info", "top_k"],
    )

    write_query = create_sql_query_chain(llm, db, prompt = few_shot_prompt)
    execute_query = CleanQuerySQLDatabaseTool(db=db)
    chain = write_query | execute_query

    return chain
