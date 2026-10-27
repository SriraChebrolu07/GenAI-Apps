import pyodbc
import pandas as pd
from dotenv import load_dotenv
import streamlit as st
from langchain.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain.chat_models import ChatOpenAI
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
import sqlalchemy

load_dotenv()


sql_server_uri = "mssql+pyodbc://SRIRAMCHEBROLU/sql main/ driver=ODBC+Driver+17+for+SQL+Server"

# Streamlit App Initialization
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo", verbose=True)
db_chain = SQLDatabaseChain.from_llm(llm, sql_server_uri, verbose=True)
memory = ConversationBufferMemory()
conversation_buf = ConversationChain(llm=llm, memory=memory)

# Streamlit UI
st.title("AI MYSQL STREAMLIT APP")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Streamlit Chat Input
chat_input = st.text_input("What is up?")
if chat_input:
    st.chat_message("user").markdown(chat_input)
    st.session_state.messages.append({"role": "user", "content": chat_input})
    result = db_chain.run(chat_input)
    with st.chat_message("assistant"):
        st.markdown(result)
    st.session_state.messages.append({"role": "assistant", "content": result})
