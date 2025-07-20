import streamlit as st
from langchain_helper import get_few_shot_db_chain,get_last_sql_query
from db_connection import get_pymysql_connection
import pandas as pd

st.set_page_config(layout="wide")


st.title("T Shirts: Database Q&A 👕")

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
        
        # Display inventory and example questions side by side
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("### Current T-Shirt Inventory")
            st.dataframe(results_df, hide_index=True, use_container_width=True)
        
        with col2:
            st.markdown("### 💡 Example Questions")
            st.markdown(
                """
                - What is the total number of t-shirts in stock?
                - How many t-shirts do we have left for nike in extra small size and white color?
                - How much is the price of the inventory for all small size t-shirts?
                - How many t-shirts are priced above $20?
                - How many white color Levi's t shirts we have available?
                - If we have to sell all the Levi’s T-shirts today. How much revenue our store will generate without discount?
                """
            )
        
except Exception as e:
    st.error(f"Error connecting to database: {e}")
finally:
    if 'connection' in locals():
        connection.close()

st.header("Ask Questions About T-Shirts")
question = st.text_input(" ")
if question:
    try:
        chain = get_few_shot_db_chain()
        
        # Execute the chain (this will also store the SQL query globally)
        response = chain.invoke({"question": question})
        
        # Get the SQL query that was just executed
        sql_query = get_last_sql_query()
        
        # Display both components
        st.header("Generated SQL Query")
        st.write(sql_query)
        
        st.header("Answer")
        st.code(response)
        
    except Exception as e:
        st.error(f"Error processing question: {e}")
