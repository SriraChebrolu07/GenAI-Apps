import streamlit as st
from langchain.chains import ConversationChain
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()

groq_api_key = os.environ['GROQ_API_KEY']

def main():
    st.title("Groq Chat App")

    st.sidebar.title('Select an LLM')
    model = st.sidebar.selectbox(
        'Choose a model',
        ['mixtral-8x7b-32768']
    )

    # Initialize chat_history attribute if not present
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Initialize messages attribute if not present
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.chat_history:
        if "role" in message:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    groq_chat = ChatGroq(
        groq_api_key=groq_api_key,
        model_name=model
    )

    conversation = ConversationChain(
        llm=groq_chat,
    )

    if prompt := st.text_input("What is up?"):
        if prompt:
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            with st.spinner("AI is typing..."):
                response = conversation(prompt)
                full_response = response['response']
                message = {'human': prompt, 'AI': full_response}
                st.session_state.chat_history.append(message)
                st.write("Chatbot:", full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})


if __name__ == "__main__":
 main()