import os
import streamlit as st
import pandas as pd
import mysql.connector
import streamlit as st
import openai
import mysql.connector
from dotenv import load_dotenv
# Set your OpenAI API key
load_dotenv()
# openai.api_key = os.getenv("OPENAI_API_KEY")

# Function to establish a connection to the MySQL database
def create_connection():
    connection = mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "localhost"),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", ""),
        database=os.getenv("MYSQL_DATABASE", "sriram1"),
    )
    return connection


# Function to fetch data from a MySQL table
def read_data(connection, table_name):
    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql(query, connection)
    return df

# Connect to MySQL
connection = create_connection()

# Specify the table you want to read
table_name = "emp"

# Read data from the specified table
data_frame = read_data(connection, table_name)

# Display the data
print(data_frame)

# Close the MySQL connection
connection.close()


# Function to generate a response using GPT-3
def generate_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None
    )
    return response.choices[0].text.strip()

# Streamlit app
def main():
    st.title("Chat with MySQL Table")

    # User input for the chat prompt
    prompt = st.text_area("You:", "")

    # Connect to MySQL
    connection = create_connection()

    if st.button("Send"):
        # Generate response using GPT-3
        response = generate_response(prompt)

        # Display the GPT-3 response
        st.text("GPT-3:, response")

        # If the response contains a query for the MySQL table
        if "select" in response.lower() and "from" in response.lower():
            # Extract table name from the response
            start_index = response.lower().find("from") + 4
            end_index = response.lower().find(" ", start_index)
            table_name = response[start_index:end_index]

            # Read data from the specified table
            data_frame = read_data(connection, table_name)

            # Display the MySQL table data
            st.write(f"Showing data from {table_name} table:")
            st.dataframe(data_frame)

    # Close the MySQL connection
    connection.close()

if __name__ == "__main__":
    main()
