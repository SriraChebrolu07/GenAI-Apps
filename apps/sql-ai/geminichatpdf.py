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

# Function to extract text from uploaded PDF
def extract_text_from_pdf(uploaded_file):
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page_num in range(len(pdf_reader.pages)):
        text += pdf_reader.pages[page_num].extract_text()
    return text

# Streamlit UI
st.set_page_config(page_title="Gemini AI gpt")

st.header("Gemini LLM Application")

# File upload UI component
uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file:
    # Extract text from uploaded PDF
    pdf_text = extract_text_from_pdf(uploaded_file)

    # Display extracted text
    st.subheader("Extracted Text from PDF")
    st.write(pdf_text)

    # Interact with Gemini LLM
    st.subheader("Ask Questions to Gemini LLM")
    user_question = st.text_input("Input: ")
    
    if st.button("Ask the question") and user_question:
        response = get_gemini_response(user_question)
        st.subheader("Gemini LLM Response")
        for chunk in response:
            st.write(chunk.text)

# Note: In this example, the chat history is not saved as a PDF. You can modify it as needed.
