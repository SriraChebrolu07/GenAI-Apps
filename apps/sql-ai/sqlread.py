import pyodbc
import pandas as pd
import streamlit as st

conn_str = ("Driver={ODBC Driver 17 for SQL Server};"

            "Server=SRIRAMCHEBROLU;"

            "Database=sql main;"

            "Trusted_Connection=yes;")

conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# cursor.execute("Select * from dummy")

df=pd.read_sql("select * from users",conn)

print(df)

# from dotenv import load_dotenv
# import streamlit as st
# from langchain.llms import OpenAI
# from langchain.utilities import SQLDatabase
# from langchain_experimental.sql import SQLDatabaseChain
# from langchain.prompts import PromptTemplate
# import openai
# from langchain.chains import create_sql_query_chain
# from langchain.chat_models import ChatOpenAI
#
# load_dotenv()
#
# db = SQLDatabase.from_uri(os.getenv("MYSQL_URI"))
# #llm = OpenAI(temperature=0, verbose=True)
# llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo",verbose=True)
# db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)
#
# if "user_input" not in st.session_state:
#     st.session_state.user_input = " "
#
# st.title("SQL&Langchain Streamlit App")
#
# user_input = st.text_input("Ask a question:", key="user_input")
# if user_input:
#     result = db_chain.run(user_input)
#     st.write(f"Response: {result}")
#
# if st.session_state.user_input:
#     st.write(f"Stored User Input: {st.session_state.user_input}")
#
#

from dotenv import load_dotenv
import streamlit as st
from langchain.llms import OpenAI
from langchain.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain.prompts import PromptTemplate
import openai
from langchain.chains import create_sql_query_chain
from langchain.chat_models import ChatOpenAI
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

load_dotenv()

#db = SQLDatabase.from_uri(os.getenv("MYSQL_URI"))
# llm = OpenAI(temperature=0, verbose=True)
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo", verbose=True)
db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)

if "user_inputs" not in st.session_state:
    st.session_state.user_inputs = []

st.title("SQL through webapp")

user_input = st.text_input("Ask a question:", key="user_input")
# Memory conversation
memory = ConversationBufferMemory()
conversation_buf = ConversationChain(llm=llm, memory=memory)

if st.button("Submit"):
    if user_input:
        # Process user input with the db_chain
        result = db_chain.run(user_input)
        st.write(f"Response: {result}")
        st.session_state.user_inputs.append(user_input)

        conversation_buf.predict(input=user_input)
        memory.load_memory_variables({})
