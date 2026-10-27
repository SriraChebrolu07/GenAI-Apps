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

    groq_chat = ChatGroq(
        groq_api_key=groq_api_key,
        model_name=model
    )

    conversation = ConversationChain(
        llm=groq_chat,
    )

    # Display chat messages
    for message in st.session_state.chat_history:
        if "role" in message:
            if message["role"] == "user":
                st.text_area(message["content"], height=100, disabled=True)
            elif message["role"] == "assistant":
                st.text_area(message["content"], height=100, disabled=True, key=message["timestamp"])

    # User input
    prompt = st.text_input("Type a message...", key="user_input")

    # Process user input
    if st.button("Send") or (prompt and st.session_state.messages and prompt != st.session_state.messages[-1]["content"]):
        if prompt:
            timestamp = st.session_state.last_timestamp if "last_timestamp" in st.session_state else 0
            timestamp += 1
            st.session_state.last_timestamp = timestamp

            st.session_state.messages.append({
                "role": "user",
                "content": prompt,
                "timestamp": timestamp
            })
            
            with st.spinner("AI is typing..."):
                response = conversation(prompt)
                full_response = response['response']

            st.session_state.messages.append({
                "role": "assistant",
                "content": full_response,
                "timestamp": timestamp
            })
            
            st.session_state.chat_history.append({
                "role": "user",
                "content": prompt,
                "timestamp": timestamp
            })
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": full_response,
                "timestamp": timestamp
            })

if __name__ == "__main__":
    main()
