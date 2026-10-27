import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
#from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, Document
from llama_index.llms.groq import Groq
from llama_index.embeddings.fastembed import FastEmbedEmbedding
from llama_index.core import Settings
from llama_parse import LlamaParse
from llama_index.core.node_parser import MarkdownElementNodeParser
from llama_index.postprocessor.flag_embedding_reranker import FlagEmbeddingReranker
from langchain_community.vectorstores import FAISS
import os

# Load environment variables
load_dotenv()
os.getenv("GOOGLE_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
LLAMA_CLOUD_API_KEY = os.getenv("LLAMA_CLOUD_API_KEY")

parsing_instruction = """
Please parse the document into structured sections and extract the relevant information into markdown format.
"""

def get_pdf_text(pdf_docs):
    text = ""
    for pdf_doc in pdf_docs:
        pdf_reader = PdfReader(pdf_doc)
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
            else:
                st.warning(f"Could not extract text from page {page.number + 1} in {pdf_doc.name}")
    st.write("Extracted Text Length:", len(text))
    return text

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=50000, chunk_overlap=10000)
    chunks = text_splitter.split_text(text)
    st.write("Number of Text Chunks:", len(chunks))
    return chunks

def process_with_google_genai(pdf_docs):
    raw_text = get_pdf_text(pdf_docs)
    if raw_text:
        text_chunks = get_text_chunks(raw_text)
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
        vector_store.save_local("faiss_index")
    else:
        st.error("No text extracted from the documents.")

def process_with_llamaparse(pdf_docs):
    raw_text = get_pdf_text(pdf_docs)
    if raw_text:
        documents = [Document(text=raw_text)]
        embed_model = FastEmbedEmbedding(model_name="BAAI/bge-base-en-v1.5")
        Settings.llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.1)
        Settings.embed_model = embed_model
        node_parser = MarkdownElementNodeParser(llm=Groq(model="llama3-8b-8192", api_key=GROQ_API_KEY), num_workers=8)
        nodes = node_parser.get_nodes_from_documents(documents)
        base_nodes, objects = node_parser.get_nodes_and_objects(nodes)
        recursive_index = VectorStoreIndex(nodes=base_nodes + objects)
        raw_index = VectorStoreIndex.from_documents(documents)
        reranker = FlagEmbeddingReranker(
            top_n=5,
            model="BAAI/bge-reranker-large",
        )

        recursive_query_engine = recursive_index.as_query_engine(
            similarity_top_k=15,
            node_postprocessors=[reranker],
            verbose=True
        )

        parser = LlamaParse(api_key=LLAMA_CLOUD_API_KEY, result_type="markdown", parsing_instruction=parsing_instruction)
        parse_result = parser.parse(documents)
        st.write("Parsed Output:", parse_result)
        return recursive_query_engine
    else:
        st.error("No text extracted from the documents.")

def get_conversational_chain():
    prompt_template = """You are an expert summary preparation writer who has an experience of over 20 years in preparing technical and functional summary documentation.
    you have to generate a summary in the below format. only respond if you know the answer don't make up things. all the below sections are mandatory, if you don't have an answer just mention "NOT DEFINED"

Client Name: Name of the client who released these requirement, this is mandatory filed, derive it from the document's first section which may be an Introduction section \n
Type of Requirement: RFI/RFQ/RFP \n
Release date: Release Date of the requirement \n
Due Date: Submission Due Date \n
Scope of Work: Detail list of all main and sub tasks in a bullet format
Tech Requirements: Technical Requirements from the document with Due dates, mention Main and Sub requirements with due dates \n
Functional Requirements: Functional Requirements from the document with Due dates, mention Main and Sub requirements with due dates \n
Resource Skills & Location requirements: Key Personnel and Location details \n
Compliance Requirements: list all clauses which company has to comply to complete the work \n
Organization Qualification Requirements:  Describe what experience(s) and expertise your organization has Budgetary Provision: List all budget related info \n
    \n\n
    Context:\n {context}?\n
    Question: \n{question}\n

    Answer:
    """

    model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.1)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
    return chain

def user_input(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    docs = new_db.similarity_search(user_question)
    st.write("Number of Documents Retrieved:", len(docs))
    chain = get_conversational_chain()
    response = chain({"input_documents": docs, "question": user_question}, return_only_outputs=True)
    return response["output_text"]

def main():
    st.set_page_config(page_title="Chat PDF")
    st.header("Chat with PDF💁")

    if "history" not in st.session_state:
        st.session_state.history = []

    st.sidebar.title("Menu: Llama parse & Google GenAI")
    pdf_docs = st.sidebar.file_uploader("Upload your PDF Files", type=["pdf"], accept_multiple_files=True)

    processing_method = st.sidebar.radio("Select Processing Method", ("Google Generative AI", "LlamaParse"))

    if st.sidebar.button("Submit & Process"):
        if pdf_docs:
            with st.spinner("Processing..."):
                if processing_method == "Google Generative AI":
                    process_with_google_genai(pdf_docs)
                else:
                    process_with_llamaparse(pdf_docs)
                st.sidebar.success("Processing complete")
        else:
            st.sidebar.warning("Please upload PDF files.")

    # Display chat history
    for entry in st.session_state.history:
        st.chat_message("user").markdown(entry['question'])
        st.chat_message("assistant").markdown(entry['answer'])

    # Input box at the bottom
    if user_question := st.chat_input("What is up?"):
        answer = user_input(user_question)
        st.session_state.history.append({"question": user_question, "answer": answer})
        st.chat_message("user").markdown(user_question)
        st.chat_message("assistant").markdown(answer)

if __name__ == "__main__":
 main()