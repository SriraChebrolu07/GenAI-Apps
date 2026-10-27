import streamlit as st
import PyPDF2
from langchain_community.embeddings import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ChatMessageHistory, ConversationBufferMemory
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

# Loading environment variables from .env file
load_dotenv()

# Function to initialize conversation chain with GROQ language model
groq_api_key = os.environ['GROQ_API_KEY']

# Initializing GROQ chat with provided API key, model name, and settings
llm_groq = ChatGroq(
    groq_api_key=groq_api_key, model_name="mixtral-8x7b-32768",
    temperature=0.2)

# Function to process PDF files and start conversation
def process_pdf_and_start_conversation(file_path):
    pdf = PyPDF2.PdfReader(file_path)
    pdf_text = ""
    for page in pdf.pages:
        pdf_text += page.extract_text()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=50)
    texts = text_splitter.split_text(pdf_text)

    embeddings = OllamaEmbeddings(model='nomic-embed-text')
    metadatas = [{"source": f"{i}-pl"} for i in range(len(texts))]

    docsearch = Chroma.from_texts(texts, embeddings, metadatas=metadatas)

    message_history = ChatMessageHistory()

    memory = ConversationBufferMemory(
        memory_key="chat_history",
        output_key="answer",
        chat_memory=message_history,
        return_messages=True,
    )

    chain = ConversationalRetrievalChain.from_llm(
        llm=llm_groq,
        chain_type="stuff",
        retriever=docsearch.as_retriever(),
        memory=memory,
        return_source_documents=True,
    )

    return chain

# Initialize Streamlit app
st.title("PDF ChatBot")

uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded_file is not None:
    chain = process_pdf_and_start_conversation(uploaded_file)

    st.success("PDF processing complete. Ask your questions!")

    # Chat interface
    user_input = st.text_input("You:", "")
    if st.button("Send"):
        if user_input.strip() != "":
            res = chain.ainvoke(user_input)
            answer = res["answer"]
            source_documents = res["source_documents"]

            st.write("Bot:", answer)

            # Process source documents if available
            if source_documents:
                st.write("Sources:")
                for source_idx, source_doc in enumerate(source_documents):
                    st.write(f"Source {source_idx + 1}: {source_doc.page_content}")