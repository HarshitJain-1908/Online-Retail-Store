import streamlit as st
import mysql.connector
import pandas as pd
import numpy as np
import helper as helper
import time as time
import random as rand

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
                st.header("Current Status")
                current=Current_Supply(x)
                if(current[0][0]=='YES'):
                    st.write('You are currently Supplying the Products')
                else:
                    st.write('You are Currently NOT Supplying any of the Products')
            else:
                st.header("Set Current Status ")
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
        st.info("Please enter your Vendor ID to sign in ")

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

    def Place_Order(id):    # Generate order --> net amount is done via triggers implemented after consist_of is filled up
        temp=helper.FindOrder_ID()
        order_id=1+temp[0][0]
        cur.execute("Insert into Orders Values (%s,curdate(),%s,%s);",(str(order_id),str(0),str(id)))

    def Assign_DeliveryAgent(id):
        n=rand.randint(1,21)
        temp=helper.FindOrder_ID()
        order_id=1+temp[0][0]
        cur.execute("Insert into delivers Values (%s,%s,%s)",(str(n),str(order_id),'NO'))

    def Add_OrderDetails(p_id,qty):
        temp=helper.FindOrder_ID()
        order_id=1+temp[0][0]
        cur.execute("Insert into consist_of Values(%s,%s,%s)",(str(order_id),str(p_id),str(qty)))

    def Modify_Inventory(p_id,qty):
        cur.execute("Update Product set Quantity=Quantity-%s where P_ID=%s",(str(qty),str(p_id)))

    def ifSubscriber(id):
        cur.execute("Select S_ID from still_active where U_ID=%s;",(id,))
        return cur.fetchall()

    def Finalise_Amount():
        cur.execute("Update Orders Set Net_Amount = %s where O_ID=%s",(str(int(float(helper.order_Value) * (1-(float(discount)/100.0)))),str(order_id)))

    def CreateAccount(id,fn,ln,mail,pin,apt_num,street_name,age_val,contact_info):
        cur.execute("Insert into Users Values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);",(str(id),str(fn),str(ln),str(apt_num),str(street_name),str(state_name),str(pin),str(mail),str(age_val),str(contact_info)))

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
    x=st.sidebar.text_input("User ID")
    temp=helper.Finduser_ID();
    user_id=1+temp[0][0];
    
    if(x!='' and (int(x)<1 or int(x)>=user_id)):
        st.subheader("No such record exists!")
    else:
       
        option=st.sidebar.selectbox("Menu ",["Create Account","Personal Information","Order History","Subscription History","Place An Order"])

        if(option=="Create Account"):
            st.header("Registration Page")
            st.subheader("New to ShopStop ? Create Account for Free")
            first,last=st.columns(2)
            fn=first.text_input("First Name ")
            ln=last.text_input("Last Name")
            email,pincode=st.columns([3,1])
            mail=email.text_input("Email Address")
            pin=pincode.text_input("PinCode (6 Digits)")

            apt,street,state=st.columns(3)
            apt_num=apt.text_input("Apartment/House Number")
            street_name=street.text_input("Street Name (Land Mark)")
            state_name=state.text_input("State")

            age,contact=st.columns(2)
            age_val=age.text_input("Age")
            contact_info=contact.text_input("Contact Number : XXX-XXX-XXXX format")
            if(len(pin)>0 and len(pin)!=6):
                st.error("Pincode Needs to be 6 digit numeric !")
            elif(len(contact_info)>0 and (len(contact_info)!=12 or contact_info.count('-')!=2 )):
                st.error("Incorrect Format of Contact Number !")
            elif(len(ln)==0 or len(fn)==0 or len(mail)==0 or len(apt_num)==0 or len(street_name)==0 or len(age)==0 or len(state_name)==0):
                st.error("All fields are mandatory to be Filled !")
            else:
                if st.checkbox("I agree to terms & conditions * ",value=False) :
                    if st.button("Submit"):
                        CreateAccount(user_id,fn,ln,mail,pin,apt_num,street_name,age_val,contact_info)
                        with st.spinner("Please Wait for a while !"):
                            time.sleep(3)
                        st.success("Your Account has been successfully Created !")
                        st.write("Your User ID is ",user_id)
                        session.commit()

        elif(option=="Personal Information"):
            st.success("Logged in with User ID : {}".format(x))
            st.header("Personal Information")
            lst=User_Info(x)
            header=["ID","First Name","Last Name","Email","Contact Number"]
            lst=pd.DataFrame(lst,columns=header)
            st.table(lst)

        elif(option=="Order History"):
            st.header("Order History")
            st.success("Logged in with User ID : {}".format(x))
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
            st.header("Subscription History ")
            st.success("Logged in with User ID : {}".format(x))
            details=Subscription_History(x)
            lst=[]
            for i in range(len(details)):
                lst.append([details[i][0],details[i][1],subscription_dict[details[i][1]][0],subscription_dict[details[i][1]][2]])
            header=["Purchase Date","Subscription ID","Subscription Duration","Price"]
            lst=pd.DataFrame(lst,columns=header)
            st.table(lst)

        else:
            st.header("Choose Category  ")
            st.success("Logged in with User ID : {}".format(x))
            product_qty=Get_Product_Qty()
            product_quantity={} #dictionary for mapping product id --> product quantity 
            for i in range(len(product_qty)):
                product_quantity[i+1]=product_qty[i]
            #Checking if active subscriber
            discount=0 
            subscriber=ifSubscriber(x)
            # st.write(subscriber[0][0])
            if(len(subscriber)==0):
                discount=0
            else:
                discount=subscription_dict[subscriber[0][0]][1][0]
            category_selected=st.selectbox("Select The Category of Product",category_lst)
            product_selected=st.selectbox("Products Available in this Category",Category_ProdName[category_selected])
            quantity_selected=st.slider("Available Quantity",0,min(int(product_quantity[productNametoID[product_selected]][0]),10),step=1)  #Max qty -->10
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
            if(discount==0):
                st.markdown('**Cart Value**: '+ str(helper.order_Value))
            else:
                st.markdown('**Cart Value _before_ Discount**: '+ str(helper.order_Value))
                st.markdown('**Cart Value _AFTER_ Discount**: '+ str(int(float(helper.order_Value) * (1-(float(discount)/100.0))))) #to be done ! 
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
                    Place_Order(int(x))     #Creating The Order with the given amount 
                    Assign_DeliveryAgent(x) #Assigning the delivery agent using random lib    
                    for product in helper.cart:
                        p_id=productNametoID[product]
                        qty=helper.cart[product][0]
                        Add_OrderDetails(p_id,qty)  #Consist_OF insertion operation and triggers usage for final amount changing
                        Modify_Inventory(p_id,qty)  #inventory modification according to order
                    if(discount):
                        Finalise_Amount()           #Changing the final amount in order table using if subscriber function --> discount > 0
                    session.commit()                # Committing the Change in the DataBase 
                    helper.cart={}
                    helper.order_Value=0

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
    x=st.sidebar.text_input("Employee ID")
    if(x==''):
        st.info("Enter your Employee ID ")
    else:
        st.success("Logged in with Employee ID : {}".format(x))
        option=st.sidebar.selectbox("Menu ",["Personal Information","Current Position"])
        if(option=="Personal Information"):
            st.header("Personal Information")
            lst=Employee_Info(x)
            header=["ID","First Name","Last Name","Email","Contact Number","Date Of Joining"]
            df=pd.DataFrame(lst,columns=header)
            st.table(df)
        else:
            st.header("Current Position")
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
    if(x==''):
        st.info("Enter Delivery_Agent ID to sign into your account !")
    else:
        st.success("Logged in with Delivery_Agent ID : {}".format(x))
        option=st.sidebar.selectbox("Menu ",["Personal Information","Order History","Deliver A Pending Order"])
        if(option=='Personal Information'):
            personal_data=DA_Info(x)
            headers=["ID","First Name ","Last Name","Email Address","Contact Number"]
            df=pd.DataFrame(personal_data,columns=headers)
            st.table(df)

        elif (option== "Order History"):
            st.header(" Order History ")
            st.write("You have delivered the following orders till date :")
            lst=Get_Order_History(x)
            header=["Order ID"]
            df=pd.DataFrame(lst,columns=header)
            st.table(df)

        else :
            st.header("Deliver A Pending Order ")
            st.write("Following is the list of pending order that you can deliver!")
            lst=Get_Pending_Order(x)
            header=["Order ID"]   
            df=pd.DataFrame(lst,columns=header)
            st.write(df)
            if(df.empty==True):
                st.write("No Pending Orders !")
            else:
                st.header("Select Order To Deliver ")
                order=st.selectbox("Choose Order ID ",df)
                submit=st.button("Deliver Select Order")
                if(submit):
                    Deliver_Order(order)
                    session.commit()
                    with st.spinner("Processing ......"):
                        time.sleep(4)
                    st.success("Order Delivered!")