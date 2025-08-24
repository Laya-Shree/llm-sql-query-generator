__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
import streamlit as st
from langchain_helper import get_few_shot_db_chain,get_last_sql_query
from db_connection import get_pymysql_connection
import pandas as pd

st.set_page_config(layout="wide")

@st.cache_data(ttl=300)
def fetch_tshirt_data():
    connection = get_pymysql_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM t_shirts")
            tshirt_results = cursor.fetchall()
            tshirt_columns = [desc[0] for desc in cursor.description]
            return pd.DataFrame(tshirt_results, columns=tshirt_columns)
    finally:
        connection.close()

@st.cache_data(ttl=300)
def fetch_discount_data():
    connection = get_pymysql_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM discounts")
            discount_results = cursor.fetchall()
            discount_columns = [desc[0] for desc in cursor.description]
            return pd.DataFrame(discount_results, columns=discount_columns)
    finally:
        connection.close()

st.title("T Shirts: Database Q&A 👕")

try:
    # Connect to database using the new module
    connection = get_pymysql_connection()
    
    # Display layout with tabs for tables and common example questions
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Create tabs for toggling between tables
        tab1, tab2 = st.tabs(["T-Shirts Inventory", "Discounts"])
        
        with tab1:
            # Convert results to DataFrame with proper columns
            tshirt_df = fetch_tshirt_data()
            st.markdown("### Current T-Shirt Inventory")
            st.dataframe(tshirt_df, hide_index=True, use_container_width=True)
    
        with tab2:
            # Convert results to DataFrame with proper columns
            discount_df = fetch_discount_data()
            st.markdown("### Current Discounts")
            st.dataframe(discount_df, hide_index=True, use_container_width=True)

    with col2:
        st.markdown("### 💡 Example Questions")
        st.markdown(
            """
            **T-Shirt Questions:**
            - What is the total number of t-shirts in stock?
            - How many t-shirts do we have left for nike in extra small size and white color?
            - How much is the price of the inventory for all small size t-shirts?
            - How many t-shirts are priced above $20?
            - How many white color Levi's t shirts we have available?
            - If we have to sell all the Levi's T-shirts today. How much revenue our store will generate without discount?
            
            **Discount Questions:**
            - What discounts are currently active?
            - Which t-shirt brands have discounts available?
            - What is the highest discount percentage available?
            - Are there any discounts for Adidas t-shirts?
            
            **Combined Questions:**
            - What would be the final price of Nike t-shirts after applying available discounts?
            - How much total revenue can we generate if we sell all inventory with current discounts?
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
