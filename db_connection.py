import pymysql
from dotenv import load_dotenv
import os
from langchain_community.utilities import SQLDatabase

def get_db_credentials():
    """Load and return database credentials from environment variables."""
    load_dotenv()
    return {
        'user': os.getenv("DB_USER"),
        'password': os.getenv("DB_PASSWORD"),
        'host': os.getenv("DB_HOST"),
        'database': os.getenv("DB_NAME")
    }

def get_pymysql_connection():
    """Create and return a PyMySQL connection."""
    credentials = get_db_credentials()
    return pymysql.connect(
        host=credentials['host'],
        user=credentials['user'],
        password=credentials['password'],
        database=credentials['database']
    )

def get_langchain_db():
    """Create and return a LangChain SQLDatabase instance."""
    credentials = get_db_credentials()
    connection_string = f"mysql+pymysql://{credentials['user']}:{credentials['password']}@{credentials['host']}/{credentials['database']}"
    return SQLDatabase.from_uri(connection_string, sample_rows_in_table_info=3) 