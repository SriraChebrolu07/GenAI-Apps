import streamlit as st
import pandas as pd
import pyodbc

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

# Streamlit app
def main():
    st.title("SSMS Database Query Viewer")

   

    # Input query
st.subheader("Enter your Query")
query_input = st.text_area("Enter your SQL query here:")

    # Execute query and display output
if st.button("Execute Query"):
        if query_input:
            st.subheader("Input Query")
            st.code(query_input, language="sql")

            st.subheader("Query Result")
            result_df = execute_query(query_input, conn_str)
            st.dataframe(result_df)

if __name__ == "__main__":
    main()
