import streamlit as st

# Set the application title
st.title("Simple Web App")

# Read the CSV file
#df = pd.read_csv("data.csv")

# Display the data frame
#st.write(df)

# Hide the data frame by default
st.checkbox("Hide data frame", value=True)

# Display a text input widget
st.text_input("Enter your name")

# Display a button widget
st.button("Submit")