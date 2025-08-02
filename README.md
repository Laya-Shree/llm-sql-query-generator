# RAG-Based Q&A System on T-Shirt Database

An AI-driven application that enables users to query a T-shirt inventory database using natural language. It leverages large language models to convert user queries into SQL statements and returns results via a user-friendly web interface.

**🌐 Live Demo:** [https://llm-sql-query-generator.streamlit.app/](https://llm-sql-query-generator.streamlit.app/)

<img width="1526" height="857" alt="image" src="https://github.com/user-attachments/assets/0886927c-70ce-4b52-8a01-2fae7ea1235f" />
<img width="1527" height="944" alt="image" src="https://github.com/user-attachments/assets/3e017f0e-2662-4c9b-b359-d72c91570455" />

## 🧾 Overview

This project uses **LangChain**, **Google Gemini 2.0 Flash**, and **Streamlit** to interpret and answer questions related to T-shirt inventory stored in a MySQL database. It demonstrates the integration of modern LLM capabilities with traditional databases to make data querying accessible to non-technical users.

## ⚙️ Features

* 🗣️ Natural Language Interface for inventory queries
* 🧠 Automatic SQL generation using few-shot examples
* 🧲 Semantic similarity search using vector embeddings (ChromaDB)
* 💡 Example-guided prompting for improved query accuracy
* 📊 Interactive database table viewer with tabs for T-Shirts and Discounts
* 🔄 Real-time SQL query display alongside results
* 💻 Clean and responsive web UI with Streamlit

## 📁 File Structure

| File                   | Description                                                 |
| ---------------------- | ----------------------------------------------------------- |
| `app.py`              | Main Streamlit application                                  |
| `langchain_helper.py` | Handles embeddings, SQL generation, and query execution     |
| `few_shots.py`        | Stores curated few-shot examples for better prompt context  |
| `db_connection.py`    | Centralized database connection management module           |
| `create_database.sql` | SQL script to create and populate the database             |
| `code.ipynb`          | Jupyter notebook with development and testing code         |

## 🗃️ Database Schema

**Tables:**
* `t_shirts`: t_shirt_id, brand, color, size, price, stock_quantity
* `discounts`: discount_id, t_shirt_id, pct_discount

**Constraints:**
* Brand: Van Huesen, Levi, Nike, Adidas
* Color: Red, Blue, Black, White  
* Size: XS, S, M, L, XL
* Price: Between 10-50
* Discount: 0-100%

## 🧠 Tech Stack

* **Streamlit** – Frontend UI with tabbed interface
* **LangChain** – Orchestration of language and tool components
* **Google Gemini 2.0 Flash** – Natural language understanding and SQL generation
* **MySQL** – Backend database with PyMySQL connector
* **ChromaDB** – Vector database for semantic retrieval of few-shot examples
* **HuggingFace Sentence Transformers** – all-MiniLM-L6-v2 embedding model
* **Tabulate** – Clean table formatting for query results
* **pysqlite3-binary** – SQLite compatibility fix for Streamlit Cloud

## 🧬 Query Processing Pipeline

1. **Input**: User enters query in natural language
2. **Similarity Search**: Retrieves most relevant few-shot examples using ChromaDB
3. **Prompt Construction**: Builds few-shot prompt with selected examples
4. **SQL Generation**: Gemini 2.0 Flash generates MySQL query via LangChain
5. **Query Execution**: Executes query on MySQL database with error handling
6. **Result Display**: Shows both generated SQL and formatted results table

## 🛠 Setup Instructions

### Prerequisites

* Python 3.11+
* MySQL Server
* Google Gemini API Key

### Environment Variables

Create a `.env` file in the project root:

```env
API_KEY=your_google_gemini_api_key
DB_USER=your_database_username
DB_PASSWORD=your_database_password
DB_HOST=your_database_host
DB_NAME=your_database_name
```

### Installation

```bash
git clone https://github.com/Laya-Shree/llm-sql-query-generator.git
pip install -r requirements.txt
```

### Run the Application

```bash
streamlit run app.py
```
