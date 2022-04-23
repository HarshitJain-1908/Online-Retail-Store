import streamlit as st
import mysql.connector
import pandas as pd
import numpy as np
import helper as helper
import time as time

user_type=st.sidebar.selectbox("Select the User",["DataBase_Admin",'User','Vendor','Employee','Delivery_Agent'])
st.title("ShOpSTop")

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
    helper.cart={}
    helper.order_Value=0
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
    if(x!=''):
        if(int(x)>21 or int(x)<1):
            st.write("Invalid Record !")
        else:
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
                    my_bar=st.progress(100)
                    for i in range(101):
                        time.sleep(0.01)
                        my_bar.progress(i)
                    st.success("Successfully Changed!")
            session.close()
    else:
        st.write("Please enter your Vendor ID to sign in ")

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
    # [ User_info , Order_History,Order_Details,Place An Order,Subscription]

    def ProductsIDtoProductName():
        cur.execute("Select P_ID,Name,Price from product ")
        return cur.fetchall()

    def User_Info(id):
        cur.execute("Select U_ID,FirstName,LastName,Email,ContactNo from User_Details where U_ID=%s",(id,))
        return cur.fetchall()

    def Get_Order_ID(id):
        cur.execute("Select O_ID,PurchaseDate,Net_Amount,DStatus,DeliveryAgent,ContactNo from Order_History where U_ID=%s",(id,))
        return cur.fetchall()

    def Get_Order_Details(id):
        cur.execute("Select P_ID,Quantity from consist_of where O_ID=%s",(id,))
        return cur.fetchall()

    def Subscription_History(id):
        cur.execute("Select PurchaseDate,S_ID from Subscription_History where U_ID=%s",(id,))
        return cur.fetchall()

    def Get_Product_Qty():
        cur.execute("select Quantity from product order by P_ID;")
        return cur.fetchall()

    cur=session.cursor()
    product_lst=ProductsIDtoProductName()
    product_dict={}         # Dictionary which contains product_id --> [product_Name,product_Price]
    productNametoID={}
    for i in product_lst:
        product_dict[i[0]]=[i[1],i[2]]
        # productNametoID[product_dict[i[0][0]]]=i[0]
        productNametoID[i[1]]=i[0]
    #Category_lst needs to made manually because else we would have to do extra work because of indexing and lexographic order default setting in select 
    category_lst=["Clothing","Footwear","Watches","Fruits & Vegetables","Snacks","Electronics","Mobiles & Computers","Musical Instruments","Kitchen Appliances","Furniture","Books","Gaming","Cosmetics","Movies","Toys","Grocery","Medicines","Luggage","Sports & Fitness","Home Decor"]
    Category_ProdID={}
    Category_ProdName={}
    i=1
    for c in category_lst:
        temp_list=[]
        temp_list2=[]
        for j in range(i,i+10):
            temp_list.append(j)
            temp_list2.append(product_dict[j][0])
        i=i+10
        Category_ProdID[c]=temp_list
        Category_ProdName[c]=temp_list2
    category_lst=pd.DataFrame(category_lst)
    subscription_dict={1:["3 Months","3%","300₹"],2:["6 Months","5%","600₹"],3:["12 Months","8%","1200₹"]}

    x=st.sidebar.text_input("User ID [ U_ID ]")
    st.success("Logged in with User ID : {}".format(x))
    option=st.sidebar.selectbox("Menu ",["Personal Information","Order History","Subscription History","Place An Order"])

    if(option=="Personal Information"):
        st.subheader("Personal Information")
        lst=User_Info(x)
        header=["ID","First Name","Last Name","Email","Contact Number"]
        lst=pd.DataFrame(lst,columns=header)
        st.table(lst)

    elif(option=="Order History"):
        st.subheader("Order History")
        lst=Get_Order_ID(x)
        order_id_list=[]
        for i in lst:
            order_id_list.append(i[0])
        header=["Order ID","Purchase Date","Net Amount","Delivery Status","Delivery_Agent","Agent Contact No."]
        lst=pd.DataFrame(lst,columns=header)
        st.table(lst)
        if(lst.empty==False):
            selected=st.selectbox("Check Detailed Summary Of Past Orders",order_id_list)
            if(st.button("Check")):  
                order_details=Get_Order_Details(selected)
                lst2=[]
                for i in range(len(order_details)):
                        sub_total=int(order_details[i][1])*int(product_dict[order_details[i][0]][1])
                        lst2.append([product_dict[order_details[i][0]][0],product_dict[order_details[i][0]][1],order_details[i][1],sub_total])
                header=["Product","Price Per Quantity(in ₹)","Quantity Bought","Sub Total"]
                df=pd.DataFrame(lst2,columns=header)
                st.table(df)

    elif option=="Subscription History" :
        st.subheader("Subscription History ")
        details=Subscription_History(x)
        lst=[]
        for i in range(len(details)):
            lst.append([details[i][0],details[i][1],subscription_dict[details[i][1]][0],subscription_dict[details[i][1]][2]])
        header=["Purchase Date","Subscription ID","Subscription Duration","Price"]
        lst=pd.DataFrame(lst,columns=header)
        st.table(lst)

    else:
        #Important Points --> We have to maintain a net order_value to be shown on frontend (trigger is used for backend)   [Done]
        #                 --> Use a slidebar for quantity to be selected 
        #                 --> We have to maintain a list containing a nested list--> [P_ID,Quantity]
        #                 --> if the above cart is not empty and submit button is entered , we insert into  order Table  
        #                 --> Note, net amount is dependent on the fact whether there is any subscription or not as well 
        #                 --> Then we insert value into consist_of table (and trigger will automatically update amount in Order_Tble)
        #                 --> Then we randomly assign any delivery agent to it with false status of delivery 
        #                 --> Run a query to check for subscription --> if present , fetch subscription id --> update the net amount insql table 
        st.subheader("Choose Category  ")
        product_qty=Get_Product_Qty()
        product_quantity={} #dictionary for mapping product id --> product quantity 
        for i in range(len(product_qty)):
            product_quantity[i+1]=product_qty[i]
       
        category_selected=st.selectbox("Select The Category of Product",category_lst)
        product_selected=st.selectbox("Products Available in this Category",Category_ProdName[category_selected])
        quantity_selected=st.slider("Available Quantity",0,int(product_quantity[productNametoID[product_selected]][0]),step=1)
        st.write("Cost per Unit = ",product_dict[productNametoID[product_selected]][1])     #Cost per unit
        sub_total=int(product_dict[productNametoID[product_selected]][1])*int(quantity_selected)    # Total cost if purchased 
        st.write("Cost of ",quantity_selected," ",product_selected," =",sub_total)
        if(st.button("Add To Cart ")==True):
            if(quantity_selected==0):
                st.error("No quantity Selected ")
            else:
                if(product_selected in helper.cart.keys()):
                    helper.order_Value+=int(quantity_selected-helper.cart[product_selected][0])*int(product_dict[productNametoID[product_selected]][1])
                    helper.cart[product_selected]=[quantity_selected,int(quantity_selected)*int(product_dict[productNametoID[product_selected]][1])]
                else:
                    helper.cart[product_selected]=[quantity_selected,int(quantity_selected)*int(product_dict[productNametoID[product_selected]][1])]
                    helper.order_Value+=sub_total
        st.markdown('**Net Amount _before_ Discount**: '+ str(helper.order_Value))
        check=st.button("Check Cart")
        if(check):
            st.info("Format is Row_Wise : Product, Quantity, Subtotal ")
            st.table(helper.cart)
        placed=st.button("Place Order")
        if(placed):
            if(helper.order_Value==0):
                st.error("No Products are Chosen ! ")
            else:
                with st.spinner("Processing Your Order"):
                    time.sleep(2)
                st.success("Order has been Successfully Placed!")
        #At last if order_placed --> flush the cart and order_Value
        #Also we need to flush the value once a new user enters --> Again maintain a global value for value of x
        # We need to flush the value if a different type of user comes in


elif user_type=='DataBase_Admin':
    session=mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="Password!",
        database="project65"
    )
    st.header("\t\t\tData Base Admin Portal")
    helper.cart={}
    helper.order_Value=0

elif user_type=='Employee':
    helper.cart={}
    helper.order_Value=0
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
    helper.cart={}
    helper.order_Value=0
    def DA_Info(id):
        cur.execute("Select * from DeliveryAgentDetails where D_ID=%s",(id,))
        return cur.fetchall()

    def Get_Order_History(id):
        cur.execute("Select O_ID from PreviousDelivery where D_ID=%s",(id,))
        return cur.fetchall()

    def Get_Pending_Order(id):
        cur.execute("Select O_ID from PendingDelivery where D_ID=%s",(id,))
        return cur.fetchall()

    def Deliver_Order(id):
        cur.execute("Update Delivers Set Dstatus=%s where O_ID=%s ",("YES",id))

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
        lst=Get_Pending_Order(x)
        header=["Order ID"]   
        df=pd.DataFrame(lst,columns=header)
        st.write(df)
        if(df.empty==True):
            st.write("No Pending Orders !")
        else:
            st.subheader("Select Order To Deliver ")
            order=st.selectbox("Choose Order ID ",df)
            submit=st.button("Deliver Select Order")
            if(submit):
                Deliver_Order(order)
                session.commit()
                with st.spinner("Processing ......"):
                    time.sleep(4)
                st.success("Order Delivered!")