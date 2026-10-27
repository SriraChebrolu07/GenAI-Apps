from flask import Flask, request, jsonify
import pyodbc
import pandas as pd

app = Flask(__name__)

conn_str = ("Driver={ODBC Driver 17 for SQL Server};"

            "Server=SRIRAMCHEBROLU;"

            "Database=sql main;"

            "Trusted_Connection=yes;")

conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# cursor.execute("Select * from dummy")

df=pd.read_sql("select * from users",conn)

print(df)


# Create a table to store query history if it doesn't exist
cursor.execute('''
    IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'query_history')
    CREATE TABLE query_history (
        id INT IDENTITY(1,1) PRIMARY KEY,
        query_text NVARCHAR(MAX) NOT NULL,
        execution_time DATETIME NOT NULL
    )
''')
conn.commit()

# Function to execute a query and store it in the query history
def execute_query(query):
    cursor.execute(query)
    conn.commit()
    cursor.execute("INSERT INTO query_history (query_text, execution_time) VALUES (?, GETDATE())", query)
    conn.commit()

# Function to get query history
def get_query_history():
    cursor.execute("SELECT TOP 10 * FROM query_history ORDER BY execution_time DESC")
    rows = cursor.fetchall()
    return [{'id': row.id, 'query_text': row.query_text, 'execution_time': row.execution_time} for row in rows]

# Flask route to execute a query
@app.route('/execute_query', methods=['POST'])
def execute_query_route():
    data = request.get_json()
    query = data['query']
    execute_query(query)
    return jsonify({"status": "success"})

# Flask route to get query history
@app.route('/query_history', methods=['GET'])
def query_history_route():
    history = get_query_history()
    return jsonify({"history": history})

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
