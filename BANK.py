import mysql.connector

# Connecting from the server
conn = mysql.connector.connect(user='root',
                               host='localhost',
                               database='bank', passwd="CHRISTAN100#")

print(conn)
cursor = conn.cursor()


def login(user, passwd):
    cursor.execute(
        "select * from credentials where username = \"" + user + "\"and password = \"" + passwd + "\";")
    val = list(cursor.fetchall())
    if val == []:
        return 0
    else:
        return int(val[0][0])


def createAcc():
    # try:
    username = input("Enter Username: ")
    password = input("Enter Password: ")
    name = input("Enter your full name: ")
    phno = input("Enter your mobile number: ")
    address = input("Enter your address: ")
    cursor.execute("select max(uid) from user;")
    val = cursor.fetchall()
    uid = val[0][0] + 1
    accno = uid + 1000
    cursor.execute("insert into user values(" + str(
        uid) + ",\"" + name + "\"," + phno + ",\"" + name + "\",\"" + address + "\")")
    conn.commit()
    cursor.execute("insert into credentials values(" + str(uid) + ",\"" + username + "\",\"" + password + "\")")
    conn.commit()
    cursor.execute("insert into account values(" + str(uid) + "," + str(accno) + ",0)")
    conn.commit()
    return 1


# except Exception:
#     return 0


def viewAccBal(uid):
    cursor.execute("select balance from account where uid=" + str(uid))
    print("\nCurrent balance: ", cursor.fetchone()[0])


def withdraw(uid):
    cursor.execute("select balance from account where uid=" + str(uid))

    amt = float(input("Enter the amount to withdraw: "))
    if int(cursor.fetchone()[0]) <= amt:
        print("insufficient balance!! ")
    else:
        cursor.execute("update account set balance=balance-" + str(amt) + " where uid=" + str(uid))
        conn.commit()
    cursor.execute("select balance from account where uid=" + str(uid))
    print("\nCurrent balance: ", cursor.fetchone()[0])


def deposit(uid):
    amt = float(input("Enter the amount to deposit: "))
    cursor.execute("update account set balance=balance+" + str(amt) + " where uid=" + str(uid))
    conn.commit()
    cursor.execute("select balance from account where uid=" + str(uid))
    print("\nCurrent balance: ", cursor.fetchone()[0])


def deleteAcc(uid):
    cursor.execute("delete from account where uid=" + str(uid))
    conn.commit()
    cursor.execute("delete from credentials where uid=" + str(uid))
    conn.commit()
    cursor.execute("delete from user where uid=" + str(uid))
    conn.commit()


def main():
    flag = 0

    while flag == 0:
        choice = int(input(
            "\n ******WELCOME TO ABC BANK****** \n\n Press 1 Login into existing account \n Press 2 to Create a new account \n :"))
        if choice == 1:
            user = input("Enter Your Username: ")
            passwd = input("Enter Your Password: ")
            uid = login(user, passwd)

            if uid == 0:
                print("NO ACCOUNT FOUND!!\nNew user?..Create one\n")
            else:
                while True:
                    menu = int(input(
                        "***MENU*** \n\n Press 1 to View Account Balance \n Press 2 to Withdraw Money \n Press 3 to Deposit Money \n Press 4 to Delete Account \n Press 0 to EXIT:"))
                    if menu == 1:
                        viewAccBal(uid)
                    elif menu == 2:
                        withdraw(uid)
                    elif menu == 3:
                        deposit(uid)
                    elif menu == 4:
                        deleteAcc(uid)
                        print("ACCOUNT DELETED!!")
                        break
                    elif menu == 0:
                        break
                    else:
                        print("Enter a valid choice")

        else:
            if createAcc():
                print("\nACCOUNT CREATED SUCCESSFULLY!!")
            else:
                print("\nACCOUNT CREATION UNSUCCESSFULL!!")
    conn.close()


main()
