import streamlit as st
import mysql.connector
import pandas as pd

user_type=st.sidebar.selectbox("Select the User",["DataBase_Admin",'User','Vendor','Employee','Delivery_Agent'])

if(user_type=='Vendor'):
    st.header("\t\t\tVendors Portal  ")
    session=mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user="Vendor",
        password="Group65@123",
        database="project65"
    )
    cur=session.cursor()
    def Vendor_Details(vendor_id):
        cur.execute("Select * from vendor where vendor.V_ID=%s;",(vendor_id,))
        return cur.fetchall()

    def Current_Supply(vendor_id):
        cur.execute("Select AStatus from availability where V_ID=%s",(vendor_id,))
        return cur.fetchall()

    def Set_Status(vendor_id,status):
        cur.execute("Update availability Set Astatus =%s where V_ID=%s",(status,vendor_id)) 

    #Taking input from the vendor 
    x=st.sidebar.text_input("Vendor ID")
    st.success("Logged in with Vendor ID : {}".format(x))

    option=st.sidebar.radio("Menu ",["Personal Information","Current Status","Set Current Status"])
    if(option=="Personal Information"):
        lst=Vendor_Details(x)  
        lst=pd.DataFrame(lst,columns=["Vendor ID","Store Name","Phone Number ","Category"])
        st.table(lst)
    elif(option=='Current Status'):
        st.subheader("Current Status")
        current=Current_Supply(x)
        if(current[0][0]=='YES'):
            st.write('You are currently Supplying the Products')
        else:
            st.write('You are Currently NOT Supplying any of the Products')
    else:
        st.subheader("Set Current Status ")
        option_chosen=st.selectbox("Select Appropriate Option ",['YES','NO']);
        sub=st.button("Submit")
        if(sub):
            Set_Status(x,option_chosen)
            session.commit()
            st.success("Successfully Changed!")
            st.balloons()
    session.close()

elif user_type=='User':
    st.header("\t\t\tWelcome To Our Store ")
    session=mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user="User",
        password="Group65@123",
        database="project65"
    )
    cur=session.cursor()


elif user_type=='DataBase_Admin':
    session=mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="Password!",
        database="project65"
    )
    st.header("\t\t\tData Base Admin Portal")

elif user_type=='Employee':
    session=mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user="Employee",
        password="Group65@123",
        database="project65"
    )
    st.header("\t\t\tEmployee Portal ")

    def Employee_Info(id):
        cur.execute("Select * from Employee_details where E_ID=%s",(id,))
        return cur.fetchall()

    def Current_Position(id):
        cur.execute("Select C_Name from View_Manager where E_ID=%s",(id,))
        return cur.fetchall()

    cur=session.cursor()
    x=st.sidebar.text_input("Employee ID [ E_ID ]")
    st.success("Logged in with Employee ID : {}".format(x))
    option=st.sidebar.selectbox("Menu ",["Personal Information","Current Position"])
    if(option=="Personal Information"):
        st.subheader("Personal Information")
        lst=Employee_Info(x)
        header=["ID","First Name","Last Name","Email","Contact Number","Date Of Joining"]
        df=pd.DataFrame(lst,columns=header)
        st.table(df)
    else:
        st.subheader("Current Position")
        lst=Current_Position(x)
        lst=pd.DataFrame(lst,columns=["Category Name"])
        if lst.empty==False:
            st.markdown("*Category Manager :*")
            st.table(lst)
        else:
            st.markdown("*Employee*")
else: 
    session=mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user="DeliveryAgent",
        password="Group65@123",
        database="project65"
    )
    st.header( "\t\t\tDelivery Agent Portal ")
    def DA_Info(id):
        cur.execute("Select * from DeliveryAgentDetails where D_ID=%s",(id,))
        return cur.fetchall()

    def Get_Order_History(id):
        cur.execute("Select O_ID from PreviousDelivery where D_ID=%s",(id,))
        return cur.fetchall()

    def Get_Pending_Order(id):
        cur.execute("Select O_ID from PendingOrders where D_ID=%s",(id,))
        return cur.fetchall()

    cur=session.cursor()
    x=st.sidebar.text_input("Delivery Agent ID (D_ID)")
    st.success("Logged in with Delivery_Agent ID : {}".format(x))
    option=st.sidebar.selectbox("Menu ",["Personal Information","Order History","Deliver A Pending Order"])
    if(option=='Personal Information'):
        personal_data=DA_Info(x)
        headers=["ID","First Name ","Last Name","Email Address","Contact Number"]
        df=pd.DataFrame(personal_data,columns=headers)
        st.table(df)

    elif (option== "Order History"):
        st.subheader(" Order History ")
        st.write("You have delivered the following orders till date :")
        lst=Get_Order_History(x)
        header=["Order ID"]
        df=pd.DataFrame(lst,columns=header)
        st.table(df)

    else :
        st.subheader("Deliver A Pending Order ")
        st.write("Following is the list of pending order that you can deliver!")
        lst=Get_Pending_Order(id)
        header=["Order ID"]   
        df=pd.DataFrame(lst,columns=header)
        st.write(df)
        order=st.selectbox("Choose Order you want to deliver")
