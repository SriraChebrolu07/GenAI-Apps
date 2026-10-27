import streamlit as st
import pandas as pd
import pyodbc
import sqlparse

# Function to execute SQL query and return a DataFrame
def execute_query(query, conn_str):
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        df = pd.DataFrame(data, columns=columns)
        return df
    except Exception as e:
        st.error(f"Error executing query: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

# Function to convert English-like query to SQL
def convert_to_sql(english_query):
    # Basic conversion using sqlparse (you may need a more sophisticated approach)
    sql_query = str(sqlparse.format(english_query, strip_comments=True))
    return sql_query

# Streamlit app with query history
def main():
    st.title("SSMS Table Viewer with Query History")

    # Database connection
    conn_str = (
        "Driver={ODBC Driver 17 for SQL Server};"
        "Server=SRIRAMCHEBROLU;"
        "Database=sql main;"
        "Trusted_Connection=yes;"
    )

    # Query input in English
    st.subheader("English Query Input")
    english_query_input = st.text_input("Enter your query in English:")

    # Convert English to SQL
    sql_query = convert_to_sql(english_query_input)

    # Query history
    query_history = st.session_state.get("query_history", [])

    # Execute query and display table
    if st.button("Execute Query"):
        if sql_query:
            st.subheader("Query Result")
            result_df = execute_query(sql_query, conn_str)
            if result_df is not None:
                st.dataframe(result_df)

                # Add to query history
                query_history.append({"query": english_query_input, "result": result_df})
                st.session_state.query_history = query_history

    # Display query history on the main page
    st.subheader("Query History")
    for i, query_info in enumerate(query_history):
        st.markdown(f"**Query {i + 1}**")
        st.text_area("Query (English)", query_info["query"], height=80, max_chars=None, disabled=True)
        st.dataframe(query_info["result"])

if __name__ == "__main__":
    main()
