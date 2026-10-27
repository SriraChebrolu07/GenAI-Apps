import os
import tempfile
import textract
import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai

# Load environment variables
load_dotenv()
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

# Model configuration
model = genai.GenerativeModel('gemini-pro')

# Function to extract text from various file types
def extract_text_from_file(file, file_type):
    with tempfile.NamedTemporaryFile(delete=False, suffix='.' + file_type) as temp_file:
        temp_file.write(file.getvalue())
        temp_file_path = temp_file.name

    if file_type == 'pdf':
        pdf_reader = PdfReader(temp_file_path)
        text = "".join(page.extract_text() for page in pdf_reader.pages)
    elif file_type == 'docx':
        text = textract.process(temp_file_path, extension='docx').decode('utf-8')
    elif file_type == 'txt':
        with open(temp_file_path, 'r', encoding='utf-8', errors='replace') as file:
            text = file.read()
    else:
        raise ValueError("Unsupported file type")
    return text

# Function to process text and create a vector store
def process_text(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    VectorDB = Chroma.from_texts(chunks, embeddings)
    return VectorDB

# Function to get a response based on document content
def get_response_from_documents(question, vector_db):
    # Query the vector store for relevant chunks
    similar_docs = vector_db.similarity_search(question, k=5)
    # Combine the text from the relevant chunks
    context = "\n\n".join(doc.page_content for doc in similar_docs)
    # Create a prompt using the context
    prompt = f"Based on the following document content, answer the question:\n\n{context}\n\nQuestion: {question}\n\nAnswer:"
    # prompt = f"""You are an expert summary preparation writer who has an experience of over 20years in preparing technical and functional summary documentation. We will provide you with an requirement under requirements heading, you have to generate a summary in the below format.
    #             Client Name: Name of the client and Department
    #             Type of Requirement: RFI/RFQ/RFP
    #             Release date: Release Date of the requirement
    #             Due Date: Submission Due Date
    #             Tech Requirements: Technical Requirements from the document with Due dates, mention Main and Sub requirements with due dates
    #             Functional Requirements: Functional Requirements from the document with Due dates, mention Main and Sub requirements with due dates
    #             Resource Skills & Location requirements: Key Personal and Location details
    #             Compliance Requirements: list all compliance requirements
    #             Organization Qualification Requirements:  Organization Qualification Requirements
    #             Budgetary Provision: List all budget related info:\n\n{context}\n\nQuestion: {question}\n\nAnswer:"""
    # Generate the response
    response = model.generate_content(prompt, stream=True)
    full_response = ""
    for chunk in response:
        full_response += chunk.text
    return full_response

# Streamlit application
def main():
    st.header("Gemini Application for chatting with Multiple Documents")
    st.sidebar.title("Chat with Documents")
    files = st.sidebar.file_uploader('Upload your Documents', type=['pdf', 'docx', 'txt'], accept_multiple_files=True)

    if files:
        combined_text = ""
        for file in files:
            file_type = file.name.split('.')[-1]
            text = extract_text_from_file(file, file_type)
            combined_text += text + "\n\n"

        VectorDB = process_text(combined_text)

        if "vector_db" not in st.session_state:
            st.session_state.vector_db = VectorDB

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask a question based on the document content"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            if "vector_db" in st.session_state:
                response = get_response_from_documents(prompt, st.session_state.vector_db)
            else:
                response = "Please upload documents to ask questions."
            message_placeholder.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()
