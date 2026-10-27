import streamlit as st
import pandas as pd
import pyodbc

# Function to execute SQL query and return a DataFrame
def execute_query(query, conn_str):
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        df = pd.DataFrame(data, columns=columns[:1])
        return df
    except Exception as e:
        st.error(f"Error executing query: {e}")
        return None  # Return None in case of an error
    finally:
        if 'conn' in locals():
            conn.close()

# Function to get table names from the database
def get_table_names(conn_str):
    query = "SELECT table_name FROM information_schema.tables WHERE table_type = 'BASE TABLE'"
    return execute_query(query, conn_str)["table_name"].tolist()

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

    # Query input
    st.subheader("SQL Query Input")
    query_input = st.text_input("Enter your SQL query here:")

    # Query history
    query_history = st.session_state.get("query_history", [])

    # Execute query and display table
    if st.button("Execute Query"):
        if query_input:
            st.subheader("Query Result")
            result_df = execute_query(query_input, conn_str)
            if result_df is not None:
                st.dataframe(result_df)

                # Add to query history
                query_history.append({"query": query_input, "result": result_df})
                st.session_state.query_history = query_history

    # Display query history on the main page, latest query on top
    st.subheader("Query History")
    for i, query_info in enumerate(reversed(query_history)):
        st.markdown(f"**Query {i + 1}**")
        st.text_area("Query", query_info["query"], height=80, max_chars=None, disabled=True)
        st.dataframe(query_info["result"])

if __name__ == "__main__":
    main()
