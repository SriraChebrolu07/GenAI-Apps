import pyodbc
import pandas as pd
#import streamlit as st

conn_str = ("Driver={ODBC Driver 17 for SQL Server};"

            "Server=SRIRAMCHEBROLU;"

            "Database=sql main;"

            "Trusted_Connection=yes;")

conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# cursor.execute("Select * from dummy")

df=pd.read_sql("select * from cars",conn)

print(df)

# #streamlit app creation

# st.title("Welcome to your SQL database")
# #user_input = st.text_input("Enter your query prompt:")
# #if user_input:
#     #if st.button("Generate and Execute Query"):
#         #st.info("Querying database...")
       

# def main():
#     st.title("Data Retreival With MySQL");

#     # Display Options for CRUD Operations
#     option=st.sidebar.selectbox("Select an Operation",("Create","Read","Update","Delete"))
#     # Perform Selected CRUD Operations
#     if option=="Create":
#         st.subheader("Create a Record")
#         name=st.text_input("Enter Name")
#         email=st.text_input("Enter Email")
#         if st.button("Create"):
#             sql= "insert into users(name,email) values(%s,%s)"
#             val= (name,email)
#             cursor.execute(sql,val)
#             conn.commit()
#             st.success("Record Created Successfully!!!")



#     elif option=="Read":
#         st.subheader("Read Records")
#         cursor.execute("select * from users")
#         result = cursor.fetchall()
#         for row in result:
#             st.write(row)



#     elif option=="Update":
#         st.subheader("Update a Record")
#         id=st.number_input("Enter ID",min_value=1)
#         name=st.text_input("Enter New Name")
#         email=st.text_input("Enter New Email")
#         if st.button("Update"):
#             sql="update users set name=%s, email=%s where id =%s"
#             val=(name,email,id)
#             cursor.execute(sql,val)
#             conn.commit()
#             st.success("Record Updated Successfully!!!")




#     elif option=="Delete":
#         st.subheader("Delete a Record")
#         id=st.number_input("Enter ID",min_value=1)
#         if st.button("Delete"):
#             sql="delete from users where id =%s"
#             val=(id,)
#             cursor.execute(sql,val)
#             conn.commit()
#             st.success("Record Deleted Successfully!!!")


# if __name__ == "__main__":
#     main()










