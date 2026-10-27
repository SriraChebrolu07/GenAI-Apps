from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
import PyPDF2  # Library for PDF handling

# Load environment variables
load_dotenv()

# Configure GenerativeAI module
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize Generative Model
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

# Function to get Gemini response
def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response

# Function to extract text chunks from uploaded PDF
def extract_text_chunks_from_pdf(uploaded_file, chunk_size=300):
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text_chunks = []
    
    for page_num in range(len(pdf_reader.pages)):
        page_text = pdf_reader.pages[page_num].extract_text()
        chunks = [page_text[i:i + chunk_size] for i in range(0, len(page_text), chunk_size)]
        text_chunks.extend(chunks)
    
    return text_chunks

# Streamlit UI
st.set_page_config(page_title="Gemini AI gpt")

st.header("Gemini LLM Application")

# File upload UI component
uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file:
    # Extract text chunks from uploaded PDF
    pdf_text_chunks = extract_text_chunks_from_pdf(uploaded_file)

    # Display extracted text chunks as conversation
    st.subheader("Chat Bot Conversation from PDF")
    for chunk in pdf_text_chunks:
        st.text(f"User: {chunk}")
        response = get_gemini_response(chunk)
        for bot_chunk in response:
            st.text(f"Bot: {bot_chunk.text}")

# Note: In this example, the chat history is not saved as a PDF. You can modify it as needed.
