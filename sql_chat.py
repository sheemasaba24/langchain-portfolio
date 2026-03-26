import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

import sqlite3
import pandas as pd
from datetime import datetime

import os
try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass
import streamlit as st
if "GROQ_API_KEY" in st.secrets:
    os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
if "TAVILY_API_KEY" in st.secrets:
    os.environ["TAVILY_API_KEY"] = st.secrets["TAVILY_API_KEY"]

st.set_page_config(page_title="SQL Database Chatbot", page_icon="🗄️", layout="wide")
st.title("🗄️ SQL Database Chatbot")
st.markdown("Ask anything about the company database in plain English!")

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Get database schema automatically
def get_schema():
    conn = sqlite3.connect("company.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    schema = ""
    for table in tables:
        table_name = table[0]
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        col_info = ", ".join([f"{col[1]} ({col[2]})" for col in columns])
        schema += f"Table: {table_name} → Columns: {col_info}\n"
    conn.close()
    return schema

# Run SQL query safely
def run_query(sql):
    try:
        conn = sqlite3.connect("company.db")
        df = pd.read_sql_query(sql, conn)
        conn.close()
        return df, None
    except Exception as e:
        return None, str(e)

# Convert question to SQL using LLM
def question_to_sql(question, schema, chat_history):
    history_text = ""
    for msg in chat_history[-4:]:
        role = "User" if msg["role"] == "user" else "Assistant"
        history_text += f"{role}: {msg['content']}\n"

    prompt = f"""You are an expert SQL assistant. Convert the user's question into a valid SQLite SQL query.

Database Schema:
{schema}

Previous Conversation:
{history_text}

Rules:
- Return ONLY the SQL query, nothing else
- No markdown, no backticks, no explanation
- Use proper JOINs when needed
- Always use LIMIT 50 max
- For aggregations use proper GROUP BY

User Question: {question}

SQL Query:"""

    llm = ChatGroq(model="llama-3.3-70b-versatile")
    response = llm.invoke([HumanMessage(content=prompt)])
    sql = response.content.strip()
    # Clean up if LLM adds backticks anyway
    sql = sql.replace("```sql", "").replace("```", "").strip()
    return sql

# Generate natural language answer from results
def generate_answer(question, sql, df):
    if df.empty:
        return "No results found for your query."

    data_summary = df.to_string(index=False)

    prompt = f"""The user asked: "{question}"

I ran this SQL query: {sql}

Results:
{data_summary}

Write a clear, friendly, conversational answer based on these results.
Include specific numbers and names from the data.
Keep it concise but complete."""

    llm = ChatGroq(model="llama-3.3-70b-versatile")
    response = llm.invoke([HumanMessage(content=prompt)])
    return response.content

# Sidebar
with st.sidebar:
    st.header("🗄️ Database Info")
    schema = get_schema()
    st.markdown("**Tables Available:**")
    st.markdown("- 👥 employees")
    st.markdown("- 📦 products")
    st.markdown("- 💰 sales")

    st.markdown("---")
    st.markdown("**💡 Try asking:**")
    st.markdown("- Who has the highest salary?")
    st.markdown("- Show all AI Engineering employees")
    st.markdown("- What is the total sales amount?")
    st.markdown("- Which product sold the most?")
    st.markdown("- Show sales by department")

    st.markdown("---")
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    # Download chat
    if st.session_state.messages:
        chat_text = f"SQL Chat Export — {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
        for msg in st.session_state.messages:
            role = "You" if msg["role"] == "user" else "Assistant"
            chat_text += f"{role}: {msg['content']}\n"
            if "sql" in msg:
                chat_text += f"SQL: {msg['sql']}\n"
            chat_text += "\n"
        st.download_button(
            label="📥 Download Chat",
            data=chat_text,
            file_name="sql_chat.txt",
            mime="text/plain"
        )

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if "sql" in msg:
            with st.expander("🔍 View SQL Query"):
                st.code(msg["sql"], language="sql")
        if "dataframe" in msg:
            with st.expander("📊 View Raw Data"):
                st.dataframe(msg["dataframe"])

# Chat input
if question := st.chat_input("Ask anything about the database..."):
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):
        with st.spinner("Converting to SQL and querying..."):
            # Step 1: Convert to SQL
            schema = get_schema()
            sql = question_to_sql(question, schema, st.session_state.messages)

            # Step 2: Run SQL
            df, error = run_query(sql)

            if error:
                answer = f"❌ There was an error running the query: {error}"
                st.error(answer)
                st.code(sql, language="sql")
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "sql": sql
                })
            else:
                # Step 3: Generate natural answer
                answer = generate_answer(question, sql, df)
                st.write(answer)

                # Show SQL and data
                with st.expander("🔍 View SQL Query"):
                    st.code(sql, language="sql")
                with st.expander("📊 View Raw Data"):
                    st.dataframe(df)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "sql": sql,
                    "dataframe": df
                })