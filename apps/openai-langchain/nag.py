import openai
#import streamlit as st
import streamlit as st
from langchain.chat_models import ChatOpenAI
# from langchain.memory import ConversationBufferWindowMemory
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from decouple import config
#import os 
#from apikey import apikey

st.title("My Streamlit App")
st.write("Welcome to My Sreamlit App")
st.sidebar.title("ChatGpt-3.5Turbo")

llm=ChatOpenAI(openai_api_key=config("OPENAI_API_KEY"))
# os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY', '')

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": m["role"], "content": m["content"]}
                      for m in st.session_state.messages], stream=True):
            full_response += response.choices[0].delta.get("content", "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# def clear_chat_history():
#     st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
#     st.sidebar.button('Clear Chat History', on_click=clear_chat_history)
# clear_chat_history()
