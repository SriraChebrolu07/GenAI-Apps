import streamlit as st
import requests

# Backend API URL
#api_url = 'http://localhost:5000'
api_url ='https://api.publicapis.org/entries'

# Streamlit app
st.title('SSMS Query History')

# Input box for entering a new query
query = st.text_area('Enter your SQL query:', '')

# Button to execute the query
if st.button('Execute Query'):
    if query:
        # Send the query to the backend for execution
        response = requests.post(f'{api_url}/execute_query', json={'query': query})
        if response.status_code == 200:
            st.success('Query executed successfully!')
        else:
            st.error('Error executing the query.')

# Display query history
st.header('Query History')
history_response = requests.get(f'{api_url}/query_history')
if history_response.status_code == 200:
    history = history_response.json()['history']
    for entry in history:
        st.write(f"ID: {entry['id']}, Query: {entry['query_text']}, Time: {entry['execution_time']}")
else:
    st.error('Error fetching query history.')
