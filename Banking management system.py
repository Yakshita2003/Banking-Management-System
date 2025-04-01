import mysql.connector
import pickle

mydb = mysql.connector.connect(user='yakshita',
                             password='YAKSHITA',
                             host='localhost',
                             auth_plugin='mysql_native_password',
                             database='BANKDB'
                              )

mycursor=mydb.cursor(buffered=True)

def Menu():         #Function to display the menu.
     print("*"*140)
     print("MAIN MENU".center(140))
     print("1. Insert Record/Records".center(140))
     print("2. Display Records as per Account Number".center(140))
     print("   a. Sorted as per Account Number".center(140))
     print("   b. Sorted as per Customer Name".center(140))
     print("   c. Sorted as per Customer Balance".center(140))
     print("3. Search Record Details as per the account number".center(140))
     print("4. Update Record".center(140))
     print("5. Delete Record".center(140))
     print("6. TransactionsDebit/Withdraw from the account".center(140))
     print("   a. Debit/Withdraw from the account".center(140))
     print("   b. Credit into the account".center(140))
     print("7. Exit".center(140))
     print("*"*140)

def MenuSort():
     print("   a. Sorted as per Account Number".center(140))
     print("   b. Sorted as per Customer Name".center(140))
     print("   c. Sorted as per Customer Balance".center(140))
     print("   d. Back".center(140))

def MenuTransaction():
     print("   a. Debit/Withdraw from the account".center(140))
     print("   b. Credit into the account".center(140))
     print("   c. Back".center(140))

def Create():
    try:
        mycursor.execute('''CREATE TABLE IF NOT EXISTS BANK (
            ACCNO INT PRIMARY KEY, 
            NAME VARCHAR(30),
            MOBILE VARCHAR(15),
            EMAIL VARCHAR(30),
            ADDRESS VARCHAR(50),
            CITY VARCHAR(20),
            COUNTRY VARCHAR(20),
            BALANCE FLOAT)''')
        print("Table Created")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

def Insert():
    while True:
        Acc = input("Enter account no:")
        Name = input("Enter Name:")
        Mob = input("Enter Mobile:")
        email = input("Enter Email:")
        Add = input("Enter Address:")
        City = input("Enter City:")
        Country = input("Enter Country:")
        Bal = float(input("Enter Balance:"))
        Rec = (Acc, Name.upper(), Mob, email.upper(), Add.upper(), City.upper(), Country.upper(), Bal)
        Cmd = "INSERT INTO BANK VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        mycursor.execute(Cmd, Rec)
        mydb.commit()
        print("Record Inserted Successfully")
        ch = input("Do you want to enter more records (Y/N):")
        if ch.lower() == 'n':
            break

def DispSortAcc():
    try:
        mycursor.execute("SELECT * FROM BANK ORDER BY ACCNO")
        S = mycursor.fetchall()
        F="%15s %15s %15s %15s %15s %15s %15s %15s %15s"
        print(F % ("ACCNO","NAME","MOBILE","EMAIL","ADDRESS","COMPLETE ADDRESS","CITY","COUNTRY","BALANCE"))
        print("="*140)
        for i in S:
            for j in i:
                print("%14s" % j, end=' ')
            print()
        print("="*140)
    except mysql.connector.Error as err:
        print(f"Error: {err}")

def DispSortName():
    try:
        mycursor.execute("SELECT * FROM BANK ORDER BY NAME")
        S = mycursor.fetchall()
        F="%15s %15s %15s %15s %15s %15s %15s %15s %15s"
        print(F % ("ACCNO","NAME","MOBILE","EMAIL","ADDRESS","COMPLETE ADDRESS","CITY","COUNTRY","BALANCE"))
        print("="*140)
        for i in S:
            for j in i:
                print("%14s" % j, end=' ')
            print()
        print("="*140)
    except mysql.connector.Error as err:
        print(f"Error: {err}")

def DispSearchAcc():
    try:
        acc = input("Enter the account number to search: ")
        mycursor.execute("SELECT * FROM BANK WHERE ACCNO = %s", (acc,))
        S = mycursor.fetchall()
        F="%15s %15s %15s %15s %15s %15s %15s %15s %15s"
        print(F % ("ACCNO","NAME","MOBILE","EMAIL", "ADDRESS","COMPLETE ADDRESS","CITY","COUNTRY","BALANCE"))
        print("="*140)
        for i in S:
            for j in i:
                print("%14s" % j, end=' ')
            print()
        print("="*140)
    except mysql.connector.Error as err:
        print(f"Error: {err}")

def Update():
    acc = input("Enter account number to update: ")
    field = input("Enter field to update (NAME/MOBILE/EMAIL/ADDRESS/CITY/COUNTRY/BALANCE): ")
    new_value = input("Enter new value: ")
    cmd = f"UPDATE BANK SET {field} = %s WHERE ACCNO = %s"
    mycursor.execute(cmd, (new_value, acc))
    mydb.commit()
    print("Record Updated Successfully")

def Delete():
    acc = input("Enter account number to delete: ")
    mycursor.execute("DELETE FROM BANK WHERE ACCNO = %s", (acc,))
    mydb.commit()
    print("Record Deleted Successfully")

def Debit():
    try:
        cmd="select * from BANK"
        mycursor.execute(cmd)
        S=mycursor.fetchall()
        print("Please Note that the money can only be debited if min balance of Rs 5000 exists")
        acc=input("Enter the account no from which the money is to be debited")
        for i in S:
           i=list(i)
           if i[0]==acc:
              Amt=float(input("Enter the amount to be withdrawn"))
              if i[7]-Amt>=7000:
                   i[7]-=Amt
                   cmd="UPDATE BANK SET BALANCE=%s WHERE ACCNO=%s"
                   val=(i[7],i[0])
                   mycursor.execute(cmd,val)
                   mydb.commit()
                   print("Amount Debited")
                   break
              else:
                   print("There must be min balance of Rs.7000")
    except:
        print("Table does not exist")

def Credit():
    try:
       cmd="select * from BANK"
       mycursor.execute(cmd)
       S=mycursor.fetchall()
       acc=input("Enter the account no TO which the money is to be Credited: ")
       for i in S:
           i=list(i)
           if i[0]==acc:
                    Amt=float(input("Enter the amount to be credited"))
                    i[7]+=Amt
                    cmd="UPDATE BANK SET BALANCE=%s WHERE ACCNO=%s"
                    val=(i[7],i[0])
                    mycursor.execute(cmd,val)
                    mydb.commit()
                    print("Amount Credited")
                    break
       else:
            print("Record Not Found")
    except:
        print("Table Doesn't exist")
while True:
    Menu()
    ch = input("Enter your Choice: ")
    if ch == "1":
        Create()
        Insert()
    elif ch == "2":
        while True:
            MenuSort()
            ch1 = input("Enter choice a/b/c/d: ")
            if ch1.lower() == 'a':
                DispSortAcc()
            elif ch1.lower() == 'b':
                DispSortName()
            elif ch1.lower() == 'd':
                break
            else:
                print("Invalid choice")
    elif ch == "3":
        DispSearchAcc()
    elif ch == "4":
        Update()
    elif ch == "5":
        Delete()
    elif ch == "6":
        while True:
            MenuTransaction()
            ch1 = input("Enter choice a/b/c: ")
            if ch1.lower() == 'a':
                Debit()
            elif ch1.lower() == 'b':
                Credit()
            elif ch1.lower() == 'c':
                break
    elif ch == "7":
        print("Exiting...")
        break
