# RAG-Based Q&A System on T-Shirt Database

An AI-driven application that enables users to query a T-shirt inventory database using natural language. It leverages large language models to convert user queries into SQL statements and returns meaningful results via a user-friendly web interface.



## 🧾 Overview

This project uses **LangChain**, **Google Gemini Pro**, and **Streamlit** to interpret and answer questions related to T-shirt inventory stored in a MySQL database. It demonstrates the integration of modern LLM capabilities with traditional databases to make data querying accessible to non-technical users.



## ⚙️ Features

* 🗣️ Natural Language Interface for inventory queries
* 🧠 Automatic SQL generation using few-shot examples
* 🧲 Semantic similarity search using vector embeddings
* 💡 Example-guided prompting for improved query accuracy
* 💻 Clean and interactive web UI with Streamlit



## 📁 File Structure

| File                  | Description                                                 |
| --------------------- | ----------------------------------------------------------- |
| `app.py`              | Streamlit app for the front end                             |
| `langchain_helper.py` | Handles DB connection, embeddings, and SQL generation logic |
| `few_shots.py`        | Stores curated few-shot examples for better prompt context  |



## 🗃️ Database Schema

* `t_shirts`: t_shirt_id, brand, size, color, price, stock
* `discounts`: (discount details linked to T-shirt IDs) discountID, t_shirt_id, pct_discount



## 🧠 Tech Stack

* **Streamlit** – Frontend UI
* **LangChain** – Orchestration of language and tool components
* **Google gemini-2.0-flash** – Natural language understanding and SQL generation
* **MySQL** – Backend database
* **ChromaDB** – Vector database for semantic retrieval
* **HuggingFace Sentence Transformers** – Embedding model for similarity search



## 🧬 Query Processing Pipeline

1. Accepts user query in plain English
2. Retrieves similar examples using vector similarity
3. Constructs a few-shot prompt with selected examples
4. Generates SQL using Gemini Flash 2.0 via LangChain
5. Executes the query on the MySQL database
6. Displays results in a clean, tabular format



## 🛠 Setup Instructions

### Prerequisites

* Python 3.7+
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

Or manually install dependencies:

```bash
pip install streamlit langchain langchain-google-genai langchain-community pymysql python-dotenv sentence-transformers chromadb
```

### Run the Application

```bash
streamlit run app.py
```


## 💡 Example Queries

* "How many white Nike T-shirts in XS are available?"
* "What is the highest discount (in dollars) on any T-shirt?"
* "How much revenue will we generate if all Levi’s T-shirts are sold with their current discounts?"





