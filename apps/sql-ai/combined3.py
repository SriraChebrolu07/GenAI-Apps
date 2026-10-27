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
st.title(" MYSQL with Fiass VDB")
pdf = st.sidebar.file_uploader('Upload your PDF Document', type='pdf')

if pdf is not None:
    text = ""
    pdf_reader = PdfReader(pdf)
    for page in pdf_reader.pages:
        text += page.extract_text()
    VectorDB = process_text(text)

if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    if prompt:
        st.chat_message("user").markdown(prompt)
        print("debuggg2")
        st.session_state.messages.append({"role": "user", "content": prompt})
        print("debuggg1")
        result = db_chain.run(prompt)
        print("result--------",type(result))

        if "Final answer here" not in result:
            st.chat_message("assistant").markdown(result)
            st.session_state.messages.append({"role": "assistant", "content": result})

        else:
            if pdf is not None:
                documents = VectorDB.similarity_search(prompt)
                chain = load_qa_chain(llm, chain_type='stuff')
                with get_openai_callback() as cost:
                    response = chain.run(input_documents=documents, question=prompt)
                    st.chat_message("assistant").markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})

            st.session_state.conversation_history.append({"role": "user", "content": prompt})
            st.session_state.conversation_history.append({"role": "assistant", "content": result})
