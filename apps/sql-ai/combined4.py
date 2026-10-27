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

mydb = SQLDatabase.from_uri(os.environ["MYSQL_URI"])
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo", verbose=True)
db_chain = SQLDatabaseChain.from_llm(llm, mydb, verbose=True)
memory = ConversationBufferMemory()

# Define the missing process_text function
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

st.title("MySQL with Fiass VDB")
pdf = st.sidebar.file_uploader('Upload your PDF Document', type='pdf')

def process_pdf(pdf):
    if pdf is not None:
        text = ""
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
        return process_text(text)
    else:
        return None

VectorDB = process_pdf(pdf)

if not st.session_state.get("conversation_history"):
    st.session_state.conversation_history = []

if not st.session_state.get("messages"):
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    if prompt:
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        result_sql = db_chain.run(prompt)

        if "Final answer here" not in result_sql and pdf is not None and VectorDB is not None:
            # Search in Fiass VDB (PDF database)
            documents = VectorDB.similarity_search(prompt)
            chain = load_qa_chain(llm, chain_type='stuff')
            with get_openai_callback() as cost:
                result_pdf = chain.run(input_documents=documents, question=prompt)

            # Combine the results from SQL and PDF searches
            result_combined = f"SQL Result: {result_sql}\n\nPDF Result: {result_pdf}"
            st.chat_message("assistant").markdown(result_combined)
            st.session_state.messages.append({"role": "assistant", "content": result_combined})

        elif "Final answer here" not in result_sql:
            # If no PDF, display only the SQL result
            st.chat_message("assistant").markdown(result_sql)
            st.session_state.messages.append({"role": "assistant", "content": result_sql})

        elif pdf is not None and VectorDB is not None:
            # If no SQL result but PDF exists, display only the PDF result
            documents = VectorDB.similarity_search(prompt)
            chain = load_qa_chain(llm, chain_type='stuff')
            with get_openai_callback() as cost:
                result_pdf = chain.run(input_documents=documents, question=prompt)

            st.chat_message("assistant").markdown(result_pdf)
            st.session_state.messages.append({"role": "assistant", "content": result_pdf})

        else:
            st.warning("No results found.")

