from langchain.document_loaders import DirectoryLoader

#directory = '/content/pets'
directory = '\Users\srira\OneDrive\Desktop\project ai

def load_docs(directory):
  loader = DirectoryLoader(directory)
  documents = loader.load()
  return documents

documents = load_docs(directory)
len(documents)

from langchain.text_splitter import RecursiveCharacterTextSplitter

def split_docs(documents,chunk_size=1000,chunk_overlap=20):
  text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
  docs = text_splitter.split_documents(documents)
  return docs

docs = split_docs(documents)
print(len(docs))

from langchain.embeddings import SentenceTransformerEmbeddings
embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

from langchain.vectorstores import Chroma
db = Chroma.from_documents(docs, embeddings)

query = "What are the different kinds of pets people commonly own?"
matching_docs = db.similarity_search(query)

matching_docs[0]


import os
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "")

from langchain.chat_models import ChatOpenAI
model_name = "gpt-3.5-turbo"
llm = ChatOpenAI(model_name=model_name)

from langchain.chains.question_answering import load_qa_chain
chain = load_qa_chain(llm, chain_type="stuff",verbose=True)

query = "What are the emotional benefits of owning a pet?"
matching_docs = db.similarity_search(query)
answer =  chain.run(input_documents=matching_docs, question=query)
answer

from langchain.chains import RetrievalQA
retrieval_chain = RetrievalQA.from_chain_type(llm, chain_type="stuff", retriever=db.as_retriever())
retrieval_chain.run(query)


#pip install  openai langchain sentence_transformers chromadb unstructured -q
