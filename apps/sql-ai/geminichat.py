from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
from fpdf import FPDF

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

# Function to generate PDF from chat history
def generate_pdf(chat_history):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for role, text in chat_history:
        pdf.cell(200, 10, txt=f"{role}: {text}", ln=True, align='L')

    pdf_output_path = "chat_history.pdf"
    pdf.output(pdf_output_path)
    return pdf_output_path

# Streamlit UI
st.set_page_config(page_title="Gemini AI gpt")

st.header("Gemini LLM Application")

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

input_question = st.text_input("Input: ", key="input")
submit_button = st.button("Ask the question")

if submit_button and input_question:
    response = get_gemini_response(input_question)
    st.session_state['chat_history'].append(("You", input_question))
    st.subheader("The Response is")
    for chunk in response:
        st.write(chunk.text)
        st.session_state['chat_history'].append(("Bot", chunk.text))

# Save chat history as PDF
save_pdf_button = st.button("Save Chat as PDF")
if save_pdf_button and st.session_state['chat_history']:
    pdf_path = generate_pdf(st.session_state['chat_history'])
    st.success(f"Chat history saved as PDF: [{pdf_path}]")

st.subheader("The Chat History is")
for role, text in st.session_state['chat_history']:
    st.write(f"{role}: {text}")
