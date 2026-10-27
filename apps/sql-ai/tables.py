import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

# Connect to MySQL database
mydb = mysql.connector.connect(
    host=os.getenv("MYSQL_HOST", "localhost"),
    user=os.getenv("MYSQL_USER", "root"),
    password=os.getenv("MYSQL_PASSWORD", ""),
    database=os.getenv("MYSQL_DATABASE", "sriram1")
)
mycursor = mydb.cursor()

# Create the 'countries' table
mycursor.execute('''
    CREATE TABLE IF NOT EXISTS countries (
        code CHAR(2) NOT NULL,
        name VARCHAR(255) NOT NULL,
        full_name VARCHAR(255) NOT NULL,
        iso3 CHAR(3) NOT NULL,
        number SMALLINT(3) ZEROFILL NOT NULL,
        continent_code CHAR(2) NOT NULL,
        PRIMARY KEY (code),
        FOREIGN KEY (continent_code) REFERENCES continents (code)
    )
''')




mycursor.executemany('''
    INSERT INTO countries (code, name, full_name, iso3, number, continent_code)
    VALUES (%s, %s, %s, %s, %s, %s)
''', countries_data)

# Commit changes and close the connection
mydb.commit()
mycursor.close()
mydb.close()

print("Table 'countries' created and data inserted successfully.")
