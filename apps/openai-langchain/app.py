import os
from tkinter import PAGES
import streamlit as st 
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS

from apikey import apikey
os.environ["OPEN_API_KEY"]= apikey

def get_pdf_text(pdf_docs):
  text = ""
  for pdf in pdf_docs:
   pdf_reader = PdfReader(pdf)
   for page in pdf_reader.pages:
       text += page.extract_text()
  return text

def get_text_chunks(text):
 text_splitter=CharacterTextSplitter( seperator="\n",chunk_size=1000,chunk_overlap=200,lenght_function=len)
 chunks=text_splitter.split_text(text)
 return chunks

def get_vectorstore(text_chunks):
 embeddings = OpenAIEmbeddings
 vectorstore = FIASS.from_texts(texts=text_chunks,embedding=embeddings)
 return vectorstore

def main():
  load_dotenv()
st.write(page_title="chat with multiple pdfs",page_icon=":books:")
st.header("chat with multiple pdfs:books:")
st.text_input("Enter a query about your PDFs:")
with st.sidebar:
  st.subheader("Your documents")
  pdf_docs = st.file_uploader("Upload your PDFs and click on PROCESS",accept_multiple_files=True)
  if st.button("PROCESS"):
   with st.spinner("Processing"):
   #get pdf text
    raw_text= get_pdf_text(pdf_docs)

    #getting the text chunks
   text_chunks = get_text_chunks(raw_text)
   st.write(text_chunks)

    #creating vectore store
  vectorstore=get_vectorstore(text_chunks)

  #creating conversation chain
  st.session_state.conversation = get_conversation_chain(vectorstore)
st.write(raw_text)


