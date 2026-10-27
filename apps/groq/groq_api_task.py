import re
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex
from llama_index.llms.groq import Groq
from llama_index.embeddings.fastembed import FastEmbedEmbedding
from llama_index.core import Settings
from llama_parse import LlamaParse
# Load your OPENAI_API_KEY from your .env file
from llama_index.postprocessor.flag_embedding_reranker import FlagEmbeddingReranker
import pickle
import os
from llama_index.core.node_parser import MarkdownElementNodeParser
load_dotenv()

# Choose the model for the agents
# model = ChatOpenAI(model_name="gpt-4-1106-preview", temperature=0.2)
llm = ChatGroq(
            api_key=os.getenv("GROQ_API_KEY"),
            model="llama3-70b-8192"
        )


LLAMA_CLOUD_API_KEY = os.getenv("LLAMA_CLOUD_API_KEY")


# Define a function to load parsed data if available, or parse if not
def load_or_parse_data():
    data_file = "./parsed_data.pkl"

    if os.path.exists(data_file):
        # Load the parsed data from the file
        with open(data_file, "rb") as f:
            parsed_data = pickle.load(f)
    else:
        # Perform the parsing step and store the result in llama_parse_documents
        parsingInstructionUber10k = """The provided document is a Statement of Work released by StaidLogic"""
        parser = LlamaParse(api_key=LLAMA_CLOUD_API_KEY, result_type="markdown", parsing_instruction=parsingInstructionUber10k)
        llama_parse_documents = parser.load_data("sl2.pdf")


        # Save the parsed data to a file
        with open(data_file, "wb") as f:
            pickle.dump(llama_parse_documents, f)

        # Set the parsed data to the variable
        parsed_data = llama_parse_documents

    return parsed_data

documents =  load_or_parse_data()

# print(documents[0].text[:1000] + '...')
print(documents[0])


# GROQ_API_KEY = os.getenv('GROQ_API_KEY')

# by default llamaindex uses OpenAI models
embed_model = FastEmbedEmbedding(model_name="BAAI/bge-base-en-v1.5")

# llm = Groq(model="mixtral-8x7b-32768", api_key= GROQ_API_KEY)

Settings.llm = llm
Settings.embed_model = embed_model

GROQ_API_KEY=os.getenv("GROQ_API_KEY")

node_parser = MarkdownElementNodeParser(llm = Groq(model="llama3-8b-8192", api_key= GROQ_API_KEY), num_workers=8)
nodes = node_parser.get_nodes_from_documents(documents)

base_nodes, objects = node_parser.get_nodes_and_objects(nodes)
recursive_index = VectorStoreIndex(nodes=base_nodes+objects)
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

raw_query_engine = raw_index.as_query_engine(similarity_top_k=15, node_postprocessors=[reranker])
query = "Get Detailed Technical Requirements"
response_1 = raw_query_engine.query(query)
print("\n**New LlamaParse+ Basic Query Engine")
print(response_1)

response_2 = recursive_query_engine.query(query)
print("\n**New LlamaParse+ Recursive Retriever Query Engine")
print(response_2)
