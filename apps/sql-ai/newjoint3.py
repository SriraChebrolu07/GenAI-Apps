import os
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
load_dotenv()
from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.chains import SimpleSequentialChain
from langchain.llms import OpenAI
from langchain.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from PyPDF2 import PdfReader
import streamlit as st
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain import FAISS
from langchain.chains.question_answering import load_qa_chain
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


st.title("AI MYSQL & VECTOR DB STREAMLIT APP")
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

prompt = st.chat_input(" what is up?")
if prompt:
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    print("prompt ", prompt)

    db = SQLDatabase.from_uri(os.environ["MYSQL_URI"])
    llm = OpenAI(temperature=0, verbose=True)
    db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)

    documents = VectorDB.similarity_search(prompt)
    chain = load_qa_chain(llm, chain_type='stuff', verbose=True)
    result = db_chain.run(prompt)
    response = chain.run(question=prompt, input_documents=documents)
    Sequential_Chain = SimpleSequentialChain(chain=[result, response], verbose=True)

    st.chat_message("assistant").markdown(Sequential_Chain)
    st.session_state.messages.append({"role": "assistant", "content": Sequential_Chain})
    st.session_state.conversation_history.append({"role": "assistant", "content": Sequential_Chain})
