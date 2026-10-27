import pyodbc
import pandas as pd
from dotenv import load_dotenv
import streamlit as st
from langchain.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain.chat_models import ChatOpenAI
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

load_dotenv()

# Streamlit App Initialization
st.title("AI MYSQL STREAMLIT APP")

# Database Connection
try:
    conn_str = (
        "Driver={ODBC Driver 17 for SQL Server};"
        "Server=SRIRAMCHEBROLU;"
        "Database=sql main;"
        "Trusted_Connection=yes;"
    )
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    st.success("Connected to the database successfully!")
except Exception as e:
    st.error(f"Failed to connect to the database. Error: {e}")
    st.stop()

# Create SQLDatabase object
sql_database = SQLDatabase(conn_str)

# Streamlit UI Layout
st.sidebar.title("Controls")
chat_input = st.sidebar.text_input("You:")

if st.sidebar.button("Submit"):
    st.session_state.messages.append({"role": "user", "content": chat_input})
    result = db_chain.run(chat_input)
    st.session_state.messages.append({"role": "assistant", "content": result})

# Display Chat Messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Close the database connection when done
conn.close()
