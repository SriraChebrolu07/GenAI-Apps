# Import necessary libraries

import streamlit as st
from textblob import TextBlob

# Streamlit app
st.title("Simple Sentiment Analysis Web App")

# Text input
text_input = st.text_area("Enter text for sentiment analysis:", "Type here...")

# Process the text with TextBlob
blob = TextBlob(text_input)
sentiment_score = blob.sentiment.polarity

# Display sentiment analysis result
if sentiment_score > 0:
    sentiment = "Positive"
elif sentiment_score < 0:
    sentiment = "Negative"
else:
    sentiment = "Neutral"

if st.button("Analyze Sentiment"):
    st.subheader("Sentiment Analysis Result:")
    st.write(f"Sentiment: {sentiment}")
    st.write(f"Sentiment Score: {sentiment_score}")

# Add a footer
st.markdown("---")
st.markdown("Built by sriram")

