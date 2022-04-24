import streamlit as st
import mysql.connector 

session=mysql.connector.connect(        #DATABASE ADMIN Account has been used 
    host="127.0.0.1",
    port=3306,
    user="root",
    password="Password!",
    database="project65"
)
cur=session.cursor()

def Finduser_ID():                  # To help find the maximum User_ID assigned in the database
    cur.execute("select max(U_ID) from users;")
    return cur.fetchall()

def FindOrder_ID():                 # To find the maximum oRder_ID punched in the database 
    cur.execute("Select max(O_ID) from orders;")
    return cur.fetchall()
    
order_Value=0   #for users_order frontend work 
cart={}         #each element --> [P_ID,Qty,subtotal]
