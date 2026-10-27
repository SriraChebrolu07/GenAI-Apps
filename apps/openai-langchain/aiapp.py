import streamlit as st
import requests
from transformers import pipeline

# Title
st.title("Simple AI App with Streamlit")

# Sidebar
st.sidebar.header("AI Model Options")
model_type = st.sidebar.selectbox("Select an AI model", ["Sentiment Analysis"])
text = st.text_area("Enter text for analysis")

# Load the selected model
if model_type == "Sentiment Analysis":
    sentiment_classifier = pipeline("sentiment-analysis")

# Function to perform sentiment analysis
def perform_sentiment_analysis(text):
    result = sentiment_classifier(text)
    return result[0]

# Display the results
if st.button("Analyze Text"):
    if text:
        with st.spinner("Analyzing..."):
            result = perform_sentiment_analysis(text)
            st.write(f"Sentiment: {result['label']}")
            st.write(f"Confidence: {result['score']:.2f}")
    else:
        st.warning("Please enter text for analysis.")

# Optional: Add more models and functionality as needed