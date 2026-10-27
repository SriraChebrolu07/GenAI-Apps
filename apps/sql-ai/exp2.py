import streamlit as st
import openai
import PyPDF2
import io

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def read_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page_num in range(len(pdf_reader.pages)):
        text += pdf_reader.pages[page_num].extract_text()
    return text

def extract_relevant_text(text, max_length=2000):
    # Truncate or summarize the text to a certain length
    return text[:max_length]

def chat_with_openai(message):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=message,
        max_tokens=150,
        n=1,
        stop=None
    )
    return response.choices[0].text.strip()

def main():
    st.title("PDF Chat App")

    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

    if uploaded_file is not None:
        st.sidebar.title("Chat with PDF")
        st.sidebar.text("Ask questions about the PDF")

        # Initialize chat history list
        chat_history = []

        pdf_text = read_pdf(uploaded_file)
        relevant_pdf_text = extract_relevant_text(pdf_text)

        user_question = st.sidebar.text_input("Ask a question:")
        if st.sidebar.button("Ask"):
            if user_question:
                st.text("You asked: {}".format(user_question))

                # Combine user question with relevant PDF text for conversation
                conversation = f"User: {user_question}\nPDF: {relevant_pdf_text}"

                # Get OpenAI response with max tokens set
                response = chat_with_openai(conversation)

                # Add conversation to chat history
                chat_history.insert(0, {"user": user_question, "response": response})

                st.text("OpenAI's response:")
                st.write(response)

            else:
                st.warning("Please enter a question.")

        # Display chat history
        st.title("Chat History")
        for chat_entry in chat_history:
            st.text(f"User: {chat_entry['user']}")
            st.text(f"OpenAI: {chat_entry['response']}")
            st.markdown("---")

    else:
        st.warning("Please upload a PDF file.")

if __name__ == "__main__":
    main()
