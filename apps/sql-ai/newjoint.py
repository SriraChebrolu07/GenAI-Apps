import os
from dotenv import load_dotenv
from PyPDF2 import PdfReader
import streamlit as st
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.callbacks import get_openai_callback
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain

load_dotenv()

db = SQLDatabase.from_uri(os.environ["MYSQL_URI"])
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo", verbose=True)
db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)
memory = ConversationBufferMemory()

def process_text(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    embeddings = OpenAIEmbeddings()
    VectorDB = FAISS.from_texts(chunks, embeddings)
    return VectorDB

st.title("mysql and faiss linked app")
pdfs = st.sidebar.file_uploader('Upload your PDF Documents', type='pdf', accept_multiple_files=True)

if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

if "messages" not in st.session_state:
    st.session_state.messages = []

VectorDBs = []
if pdfs:
    for pdf in pdfs:
        text = ""
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
        VectorDB = process_text(text)
        VectorDBs.append(VectorDB)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

combined_query = st.chat_input(" what is up?")
if combined_query:
    st.chat_message("user").markdown(combined_query)
    st.session_state.messages.append({"role": "user", "content": combined_query})

    queries = combined_query.split('and')

    for query in queries:
        result = db_chain.run(query.strip())
        if "Final answer here" in result:
            break

    else:
        for VectorDB in VectorDBs:
            documents = VectorDB.similarity_search(query)
            chain = load_qa_chain(llm, chain_type='stuff')
            with get_openai_callback() as cost:
                response = chain.run(input_documents=documents, question=query)
                break  # assuming you only want to run the QA chain once

        st.chat_message("assistant").markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.session_state.conversation_history.append({"role": "user", "content": combined_query})
        st.session_state.conversation_history.append({"role": "assistant", "content": response})
