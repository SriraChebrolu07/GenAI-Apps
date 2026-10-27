import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

mydb = mysql.connector.connect(
    host=os.getenv("MYSQL_HOST", "localhost"),
    user=os.getenv("MYSQL_USER", "root"),
    password=os.getenv("MYSQL_PASSWORD", ""),
    database=os.getenv("MYSQL_DATABASE", "sriram1")
)
mycursor=mydb.cursor()
print("Connection Established")

#mycursor.execute("CREATE TABLE customers (id int, name VARCHAR(20), salary int)")
#mycursor.execute("CREATE TABLE emp (name VARCHAR(255), address VARCHAR(255))")
#mycursor.execute("CREATE TABLE students (id int, name VARCHAR(25), gender VARCHAR(25))")
mycursor.execute("CREATE TABLE movies (id int, name VARCHAR(25), release VARCHAR(25), status varchar(20))")
sql = "INSERT INTO movies (id,name, release, status) VALUES (%s,%s, %s,%s)"
val = [
  (1,'Interstellar', '2014','Blockbuster'),
  (2,'Dark Knight', '2008','Blockbuster'),
  (3,'Lucy', '2014','success'),
  (4,'Topgun maverick', '2022','blockbuster'),
  (5,'Kingsman', '2014','superhit'),
  (6,'Terminator5', '2003','failure'),
  (7,'Hungergames', '2011','success'),
  
]

mycursor.executemany(sql, val)

mydb.commit()

print(mycursor.rowcount, "was inserted.")
