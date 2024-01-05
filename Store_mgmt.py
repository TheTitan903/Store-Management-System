#importing mysql.connector to connect to database
import random
import mysql.connector as ms
db1= ms.connect(host="localhost",user="root",passwd="Surya123",database="shuddaorganicstore")
mycursor=db1.cursor()

#function to print welcome page
def welcome():
    print("WELCOME TO SHUDDHA ORGANIC STORE")
welcome()

#function to enter as admin or user
def Enter():
    print("Are you a customer or admin?")
    entry=input("If you are a customer enter 1 or if you are an admin enter 2:")
    if entry=="2":
        adminname=[]
        adminemail=[]
        mycursor.execute("select AdminUser_Name from adminusers")
        for data in mycursor:
            adminname.extend(data)
        mycursor.execute("select Admin_Email from adminusers")
        for data in mycursor:
            adminemail.extend(data)
        name=input("Enter your Name:")
        if name in adminname:
            otp=random.randint(1000,9999)
            otpstr=str(otp)
            l=len(adminname)
            for i in range(l):
                if adminname[i]==name:
                    receivermail=adminemail[i]
                    break
            import smtplib
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()
            s.login("shuddaorganic@gmail.com", "maharishi")
            message = "Dear Admin, Welcome back to ShuddaOrganic Store!!! The one Time Password for your login is {}".format(otp)
            s.sendmail("shuddaorganic@gmail.com", receivermail, message)
            s.quit() 
            print("You have received an email in your registered email id")
            otpin=input("Enter the one time passwword:")
            if otpin==otpstr:
                print("Welcome")
                admin()
            else:
                print("Incorrect otp")
                Enter()
        else:
            print('Invalid Name')
            Enter()         
    elif entry=="1":
         print("Welcome")
         display()
    else:
        print("Invalid Input")
        Enter()
import mysql.connector as ms
db1= ms.connect(host="localhost",user="root",passwd="Surya123",database="shuddaorganicstore")
mycursor=db1.cursor()

#function to display options when admin logs in
def admin():
    print("What do you want to do?")
    print("If you want to add an item enter 1")
    print("Or if you want to generate the list of items which need to be re-ordered enter 2")
    choice1()

def choice1():
    choice=input("Enter your choice")
    if choice=="1":
        add_new()
    elif choice=="2":
        roq_rol()
    else:
        print("Invalid choice")
        choice1()

#Function for admin to add a new item in Items table            
def add_new():
    itemname=input("Enter the name of the item you want to add:")
    itemdesc=input("Enter the description of item you want to add:")
    itemqty(itemname,itemdesc)

def itemqty(itemname,itemdesc):
    test=input("Enter the quantity of the item(in kg/litre):")
    itemquantity=test.replace('.', '', 1)
    if itemquantity.isdigit():
        itemcost1=itemcost()
        itemreorderquantity=itemroq()
        itemreorder=itemrol()
        rol_check(itemquantity,itemcost1,itemreorder,itemreorderquantity,itemname,itemdesc)
    else:
        print("Invalid item quantity")
        itemqty(itemname,itemdesc)

def itemcost():
    test=input("Enter the cost of item:")
    itemcostv=test.replace('.', '', 1)    
    if itemcostv.isdigit():
          return itemcostv
    else:
        print("Invalid cost,Please enter numeric value")
        itemcost()

def itemrol():
    test=input("Enter the re order level of item:")
    itemreorderl=test.replace('.', '', 1)    
    if itemreorderl.isdigit():
        print(" ")
    else:
        print("Invalid item re order level")
        itemreorderl=itemrol()
    return itemreorderl   

def itemroq():
    itemreorderquantity=input("Enter the re order quantity of item:")
    test=itemreorderquantity.replace('.', '', 1)
    if test.isdigit():
        return (test)
    else:
        print("Invalid re order quantity,Please enter a numeric value")
        itemroq()

def rol_check(itemquantity,itemcost,itemreorderlevel,itemreorderquantity,itemname,itemdesc):
    if float(itemquantity)>float(itemreorderlevel) and float(itemreorderquantity)>float(itemreorderlevel):
        mycursor.execute("select count(*) from productmaster")
        num= mycursor.fetchone()
        num=int(num[0]) +1
        length=len(str(num))
        if length==1:
            prodid="P"+"00"+str(num)
        elif length==2:
            prodid="P"+"0"+str(num)
        else:
            prodid="P"+str(num)
        query= "insert into productmaster values( '{0}', '{1}', '{2}', {3} ,{4} ,{5},{6})".format(prodid,itemname,itemdesc, itemquantity,itemcost,itemreorderlevel,itemreorderquantity)
        mycursor.execute(query)
        db1.commit()
        print("New item added successfully")
        
    else:
        print("Item quantity or Item reorder quantity is less than the reorder level!! Please check.")
        itemreorderlevel=itemrol()
        rol_check(itemquantity,itemcost,itemreorderlevel,itemreorderquantity,itemname,itemdesc)

def roq_rol():
    reorderlist=[]
    mycursor.execute("select Prod_Name from productmaster where Prod_Qty < Product_ROL")
    for data in mycursor:
        reorderlist.extend(data)
        print(data)
    if reorderlist:
        admchoice(reorderlist)
    else:
        print("All items are available as per requirement")
        admin()

def admchoice(reorderlist):
    print("If you want to re order the above items press 1")
    print("Or if you want to return to the menu press 2")
    adminchoice=input("Enter your choice")
    if adminchoice=="1":
        for data in reorderlist:
            query="update productmaster set Prod_Qty = Prod_Qty + Product_ROQ where Prod_Name = '%s'" % (data,)
            mycursor.execute(query)
            db1.commit()
            print("%s was re ordered successfully" % data )
        
    elif adminchoice=="2":
        admin()
    else:
        print("Invalid choice")
        admchoice()
import mysql.connector as ms
db1= ms.connect(host="localhost",user="root",passwd="Surya123",database="shuddaorganicstore")
mycursor=db1.cursor()
global currentcost
currentcost=0

def display():
    mycursor.execute("select Product_Id,Prod_Name,Prod_Desc from productmaster")
    for data in mycursor:
        print(data)
    select()

def select():
    product=input("Please enter the product id of the item you want to purchase:")
    prodid_chk(product)

def prodid_chk(product):
    mycursor.execute("select Product_Id from productmaster")
    lst=[]
    for data in mycursor:
        lst.extend(data)
    product= product.upper()
    if product in lst:
        quantity(product)
    else:
        print("Invalid product id")
        select()

def quantity(product):
    test=input("Please enter the quantity of the item you need in kg/litres:")
    custquantity=test.replace('.', '', 1)
    if custquantity.isdigit():
        quantity_chk(custquantity,product)
    else:
        print("Invalid item quantity")
        quantity()

def quantity_chk(custquantity,product):
    query = "select Prod_Qty from productmaster where Product_Id = '%s'"%(product)
    mycursor.execute(query)
    prodqty=mycursor.fetchone()
    if int (custquantity) <prodqty[0]:
        custchoice(product,custquantity)
        #transaction(product,custquantity)
    else:
        print("The quantity of good available is less than your order. Please enter a lesser quantity")
        quantity(product)

def transaction(product,custquantity):
    print("Your order has been placed successfully")
    query= "update productmaster set Prod_Qty = Prod_Qty-%d where Product_Id= '%s'"%(int(custquantity),product)
    mycursor.execute(query)
    db1.commit()
    query = "select Prod_Cost from productmaster where Product_Id = '%s'"%(product)
    mycursor.execute(query)
    itemcost=mycursor.fetchone()
    cost=int(itemcost[0])*float(custquantity)
    return cost

def custchoice(product,custquantity):
    print("If you want to shop more press 1")
    print("Else if you want to stop shopping press 2")
    choice=input("Enter your choice")
    if choice=="1":
        totalcost(product,custquantity)
        display()
    elif choice=="2":
        cost=totalcost(product,custquantity)
        payment(cost)
    else:
        print("Invalid choice")
        custchoice()

def payment(cost):
    print("The cost of your purchase is",cost)
    cardno=input("Please enter your card number")
    if cardno.isdigit():
        print("Payment made successfully")
        print("Thank you for shopping with us")
        #transtable()
    else:
        print("Invalid card number")
        payment(cost)

def totalcost(product,custquantity):
    global currentcost
    cost = transaction(product,custquantity)
    currentcost+=  cost
    return currentcost
    
Enter()