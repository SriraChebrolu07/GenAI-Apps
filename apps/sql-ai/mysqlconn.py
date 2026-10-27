# import mysql.connector
# import pandas as pd
# import streamlit as st

# # Establish a connection to MySQL Server


# #mydb = mysql.connector.connect(
#    # host="localhost",
#     #user="root",
#     #password=os.getenv("MYSQL_PASSWORD"),
#     #database="sriram1",
    
# #)
# #mycursor=mydb.cursor()
# #print("Connection Established")

# #df=pd.read_sql("select * from students",mydb)

# #print(df)


from dotenv import load_dotenv
import os
import streamlit as st
from langchain.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain.chat_models import ChatOpenAI
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
import sqlalchemy
load_dotenv()

db_uri = os.getenv("MYSQL_URI", "mysql+pymysql://user:password@localhost:3306/database")
mydb = SQLDatabase.from_uri(db_uri)
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo", verbose=True)
db_chain = SQLDatabaseChain.from_llm(llm, mydb, verbose=True)
memory = ConversationBufferMemory()
conversation_buf = ConversationChain(llm=llm, memory=memory)

if "user_inputs" not in st.session_state:
    st.session_state.user_inputs = []

if "assistant_responses" not in st.session_state:
    st.session_state.assistant_responses = []

st.title("AI MYSQL STREAMLIT APP")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    if prompt:
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        result = db_chain.run(prompt)
        with st.chat_message("assistant"):
            st.markdown(result)
        st.session_state.messages.append({"role": "assistant", "content": result})
#mydb.close()
