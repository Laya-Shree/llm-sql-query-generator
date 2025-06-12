import streamlit as st
from langchain_helper import get_few_shot_db_chain
from db_connection import get_pymysql_connection
import pandas as pd
st.title("T Shirts: Database Q&A 👕")

st.header("Current T-Shirt Inventory")
try:
    # Connect to database using the new module
    connection = get_pymysql_connection()
    
    with connection.cursor() as cursor:
        # Execute query to get all t-shirts
        cursor.execute("SELECT * FROM t_shirts")
        results = cursor.fetchall()
        
        # Get column names
        columns = [desc[0] for desc in cursor.description]
        
        # Convert results to DataFrame with proper columns
        results_df = pd.DataFrame(results, columns=columns)
        
        # Display the DataFrame without index
        st.dataframe(results_df, hide_index=True)
        
except Exception as e:
    st.error(f"Error connecting to database: {e}")
finally:
    if 'connection' in locals():
        connection.close()


st.header("Ask Questions About T-Shirts")
question = st.text_input("Question: ")

if question: 
    chain = get_few_shot_db_chain()
    response = chain.invoke({"question":question})

    st.header("Answer")
    st.write(response)
