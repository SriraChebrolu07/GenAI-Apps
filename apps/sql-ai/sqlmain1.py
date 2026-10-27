import streamlit as st
import pandas as pd
import pyodbc

# Function to execute SQL query and return a DataFrame
def execute_query(query, conn_str):
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    df = pd.DataFrame(data, columns=columns[:1])
    conn.close()
    return df

# Streamlit app with chat history
def main():
    st.title("SSMS Database Query Viewer")

    # Database connection details
conn_str = ("Driver={ODBC Driver 17 for SQL Server};"

            "Server=SRIRAMCHEBROLU;"

            "Database=sql main;"

            "Trusted_Connection=yes;")

conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# cursor.execute("Select * from dummy")

df=pd.read_sql("select * from users",conn)

print(df)

    # Input query
st.subheader("Input Query")
query_input = st.text_area("Enter your SQL query here:")

    # Chat history list
chat_history = []

    # Execute query and display output
if st.button("Execute Query"):
        if query_input:
            st.subheader("Input Query")
            st.code(query_input, language="sql")

            st.subheader("Query Result")
            result_df = execute_query(query_input, conn_str)
            st.dataframe(result_df)

            # Add to chat history
            chat_history.append({"input": query_input, "output": result_df})

    # Display chat history
st.sidebar.header("Chat History")
for i, chat in enumerate(chat_history):
        st.sidebar.markdown(f"**Query {i + 1}**")
        st.sidebar.text_area("Input", chat["input"], key=f"input_{i}", disabled=True)
        st.sidebar.dataframe(chat["output"], key=f"output_{i}")

if __name__ == "__main__":
    main()
