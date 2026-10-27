from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
import fitz  # PyMuPDF for PDF handling
from io import BytesIO

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response

def read_pdf(file):
    pdf_bytes = file.read()
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    text = ""
    for page_num in range(doc.page_count):
        page = doc[page_num]
        text += page.get_text()
    return text

st.set_page_config(page_title="Gemini AI PDF Chat")

st.header("Gemini AI PDF Chat")

# Upload PDF file
pdf_file = st.file_uploader("Upload a PDF file", type=["pdf"])

# Chat Interface
st.subheader("Chat Interface")

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

input_text = st.text_input("Input: ", key="input_chat")
submit_chat = st.button("Ask the question")

if pdf_file is not None:
    if submit_chat and input_text:
        response_chat = get_gemini_response(input_text)
        st.session_state['chat_history'].append(("You", input_text))
        st.subheader("The Response is")
        for chunk in response_chat:
            st.write(chunk.text)
            st.session_state['chat_history'].append(("Bot", chunk.text))

    # Display Chat History
    st.subheader("The Chat History is")

    for role, text in st.session_state['chat_history']:
        st.write(f"{role}: {text}")
else:
    st.warning("Please upload a PDF file to use the chat.")
