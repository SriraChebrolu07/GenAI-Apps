# import streamlit as st
# from nltk.sentiment import SentimentIntensityAnalyzer
# import nltk



# # Function to perform sentiment analysis
# def analyze_sentiment(text):
#     sid = SentimentIntensityAnalyzer()
#     sentiment_score = sid.polarity_scores(text)['compound']

#     if sentiment_score >= 0.05:
#         return 'Positive'
#     elif sentiment_score <= -0.05:
#         return 'Negative'
#     else:
#         return 'Neutral'


# # Streamlit app
# def main():
#     st.title("Simple Sentiment Analysis with Streamlit")

#     # Input text area
#     user_input = st.text_area("Enter text for sentiment analysis:", "")

#     if st.button("Analyze"):
#         if user_input:
#             # Perform sentiment analysis
#             sentiment = analyze_sentiment(user_input)

#             # Display the result
#             st.write("Sentiment:", sentiment)
#         else:
#             st.warning("Please enter some text.")


# # Run the app
# if __name__ == "__main__":
#  main()





















import requests

def check_web(url):

  try:
     response=requests.get(url)
     if response.status_code==200:
        print("website is up and running")
     else:
        print(f'{url} returned {response.status_code}')

  except Exception as e:
    print(f"The error is {e}")

  finally:
     print("URL check completed")


check_web(https://www.amazon.com/)