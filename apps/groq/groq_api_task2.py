import re
import os
import pickle
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, Settings
from llama_index.llms.groq import Groq
from llama_index.embeddings.fastembed import FastEmbedEmbedding
from llama_parse import LlamaParse
from llama_index.postprocessor.flag_embedding_reranker import FlagEmbeddingReranker
from llama_index.core.node_parser import MarkdownElementNodeParser
from langchain_groq import ChatGroq

# Load environment variables
load_dotenv()

# Initialize the language model
llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama3-70b-8192"
)

LLAMA_CLOUD_API_KEY = os.getenv("LLAMA_CLOUD_API_KEY")

# Function to load or parse data
# Load or parse data
def load_or_parse_data():
    data_file = "./parsed_data.pkl"
    if os.path.exists(data_file):
        with open(data_file, "rb") as f:
            parsed_data = pickle.load(f)
    else:
        parsingInstructionUber10k = "The provided document is a Statement of Work released by StaidLogic"
        parser = LlamaParse(api_key=LLAMA_CLOUD_API_KEY, result_type="markdown", parsing_instruction=parsingInstructionUber10k)
        llama_parse_documents = parser.load_data("RFI 23-088 Third Party Administrator (TPA) DHCS.pdf")
        with open(data_file, "wb") as f:
            pickle.dump(llama_parse_documents, f)
        parsed_data = llama_parse_documents
    return parsed_data

documents = load_or_parse_data()

if documents:  # Check if documents list is not empty
    print(documents[0])  # Print first document for debugging
else:
    print("No documents found or parsed.")

# Set up embedding model
embed_model = FastEmbedEmbedding(model_name="BAAI/bge-base-en-v1.5")

Settings.llm = llm
Settings.embed_model = embed_model

# GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Node parser initialization
node_parser = MarkdownElementNodeParser(llm=Groq(model="llama3-8b-8192", api_key=GROQ_API_KEY), num_workers=8)
nodes = node_parser.get_nodes_from_documents(documents)

base_nodes, objects = node_parser.get_nodes_and_objects(nodes)
recursive_index = VectorStoreIndex(nodes=base_nodes + objects)
raw_index = VectorStoreIndex.from_documents(documents)

# Set up reranker
reranker = FlagEmbeddingReranker(
    top_n=5,
    model="BAAI/bge-reranker-large",
)

# Query engines initialization
recursive_query_engine = recursive_index.as_query_engine(
    similarity_top_k=15,
    node_postprocessors=[reranker],
    verbose=True
)

raw_query_engine = raw_index.as_query_engine(similarity_top_k=15, node_postprocessors=[reranker])

# Add prompt to the query
# prompt = "What are the detailed technical requirements for the project?"
# query = "Get Detailed Technical Requirements"
# full_query = f"{prompt} {query}"

# Execute queries and print responses
response_1 = raw_query_engine.query(full_query)
print("\n**New LlamaParse+ Basic Query Engine")
print(response_1)

response_2 = recursive_query_engine.query(full_query)
print("\n**New LlamaParse+ Recursive Retriever Query Engine")
print(response_2)
