import os
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import streamlit as st
from PyPDF2 import PdfReader

# Load environment variables
load_dotenv()

def process_text(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_db = Chroma.from_texts(text_chunks, embeddings)
    return vector_db

def extract_text_from_pdf(file):
    text = ""
    pdf_reader = PdfReader(file)
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def query_vector_db(vector_db, query):
    response = vector_db.similarity_search(query, k=1)
    if response:
        return response[0].page_content  # Access the text content properly
    return "No relevant information found in the document."

def main():
    st.header("Gemini Application for PDF Documents")
    st.sidebar.title("Chat with PDFs")
    file = st.sidebar.file_uploader('Upload your PDF', type=['pdf'])

    vector_db = None
    if file:
        text = extract_text_from_pdf(file)
        if text:
            text_chunks = [chunk.strip() for chunk in text.split('\n\n') if chunk.strip()]
            vector_db = process_text(text_chunks)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if st.session_state.get("messages") is None:
        st.session_state.messages = []

    if vector_db and (prompt := st.text_input("Ask something about the PDF")):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            loading_placeholder = st.empty()
            loading_placeholder.markdown("Thinking...")
            response = query_vector_db(vector_db, prompt)
            loading_placeholder.empty()  # Clear loading message
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()
