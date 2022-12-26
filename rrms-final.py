#IMPORTING MODULES
import sys,time
import mysql.connector as sql
from colorama import Fore
from colorama import init
init(autoreset=True,strip=True)

#SETTING UP SQL CONNECTIVITY
con=sql.connect(host="localhost",user='root',password='sql123')
cur=con.cursor()
cur.execute("show databases")
a=cur.fetchall()
flag=0
for i in a:
    if i[0]=='rrms':
        flag=1
        break
if flag==0:
    print(Fore.YELLOW+"Setting up MySQL database, please wait...")

    cur.execute("create database RRMS")
    con.commit()
    cur.execute("use RRMS")
    cur.execute("create table account(username varchar(20) primary key, password varchar(8), name varchar(20),age varchar(5), pno varchar(11),balance int)")
    cur.execute("create table available(train_no int primary key , seats int, end varchar(25), start varchar(25), price int, time varchar(25), duration varchar(20))")
    cur.execute("create table waitlist(train_no int,seats int,username varchar(20))")
    cur.execute("create table trains(train_no int primary key, route varchar(100))")
    con.commit()
    cur.execute('''insert into trains values(34387,'["Navi Mumbai","Pune","Kalaburagi","Zaheerabad","Hyderabad"]')''')
    cur.execute('''insert into trains values(67480,'["Delhi","Rohtak","Jind","Ludhiana","Jalandhar","Amritsar"]')''')
    cur.execute('''insert into trains values(79883,'["Chennai","Chittor","Bengaluru","Mandya","Mysore"]')''')
    con.commit()
    cur.execute("insert into available values(34387,150,'Hyderabad','Mumbai',900,'7:00 am, 03/03/2022','3hrs 15min')")
    cur.execute("insert into available values(67840,130,'Amritsar','Delhi',1050,'3:00 pm, 27/02/2022','2hrs 55min')")
    cur.execute("insert into available values(79883,120,'Mysore','Chennai',750,'10:00 am, 15/02/2022','2hrs 15min')")
    con.commit()

#FUNCTION DEFINITIONS
def create_account():

    username=input("Enter username: ")
    password=input("Enter password(8 CHARACTERS MAX):")
    name=input("Enter name of user: ")
    age=int(input("Enter age of user: "))
    pno=int(input("Enter phone number: "))
    try:
        cur.execute("insert into account values('%s','%s','%s','%s','%s',0)"%(username,password,name,age,pno))
        con.commit()
        cur.execute("create table "+username+"(train_no int,seats int, status varchar(20))")
        global u
        u=username
        menu()
    except:
        print(Fore.RED+"Username unavailable")
        create_account()

def booking():
    global u
    try:
        print(Fore.YELLOW+"AVAILABLE TRAINS: ")
        cur.execute("select * from available")
        a=cur.fetchall()
        print(Fore.YELLOW+"{:10}{:7}{:10}{:10}{:7}{:22}{:24}".format("TRAIN NO","SEATS","TO","FROM","PRICE","DEPARTURE TIME","DURATION"))
        print(Fore.BLUE+"="*77)
        for i in a:
            print(Fore.CYAN+"{:<10}{:<7}{:<10}{:<10}{:<7}{:<22}{:<24}".format(i[0],i[1],i[2],i[3],i[4],i[5],i[6]))
        print()
        print(Fore.RED+"*Negative seats indicate waitlisted seats")
        print(Fore.BLUE+"="*77)
        print()
        print()
        n=int(input("Enter train number you wish to book: "))
        s=int(input("Enter number of seats you wish to book: "))
        cur.execute("select * from available where train_no=%s"%(n,))
        c=cur.fetchone()
        a,b=c[1],c[4]
        cur.execute("update available set seats=%s where train_no=%s"%(a-s,n))
        if a>0 and a-s>=0:
            cur.execute("insert into %s values(%s,%s,'Booked')"%(u,n,s))
            con.commit()
        if a>0 and s>a:
            cur.execute("insert into %s values(%s,%s,'Booked')"%(u,n,a))
            cur.execute("insert into waitlist values(%s,%s,'%s')"%(n,s-a,u))
            cur.execute("insert into %s values(%s,%s,'Waitlisted')"%(u,n,s-a))
            con.commit()
        if a<=0:
            cur.execute("insert into %s values(%s,%s,'Waitlisted')"%(u,n,s))
            cur.execute("insert into waitlist values(%s,%s,'%s')"%(n,s,u))
        cur.execute("update account set balance=balance+%s where username='%s'"%(s*b,u))
        con.commit()
        print(Fore.GREEN+"Booking Successfully")
        print(Fore.GREEN+"Amount to be paid: "+str(s*b))
    except:
        print(Fore.RED+"--------------------------")
        print(Fore.RED+"|     ERROR OCCURED      |")
        print(Fore.RED+"| RETURNING TO MAIN MENU |")
        print(Fore.RED+"--------------------------")
        return


def login():
    try:
        username=input("Enter username: ")
        p=input("Enter password: ")
        cur.execute("select * from account")
        a=cur.fetchall()       #LIST OF TUPLES
        for i in a:
            if i[0]==username and i[1]==p:
                global u
                u=username
                print(Fore.GREEN+"Welcome Back")
                menu()
                break
        else:
            print(Fore.RED+"Invalid Credentials")
            print(Fore.RED+"Try Again")
            start()
    except:
        print(Fore.RED+"--------------------------")
        print(Fore.RED+"|     ERROR OCCURED      |")
        print(Fore.RED+"|RETURNING TO LOGIN MENU |")
        print(Fore.RED+"--------------------------")
        start()

def slowprint(text):
    for char in text + "\n":
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(1./10)


def start():
    cur.execute("use rrms")
    print("Press a to login into an existing account")
    print("Press b to create a new account")
    print(Fore.MAGENTA+"Enter your choice: ", end=" ")
    x=input()
    if x=='a':
        login()
    elif x=='b':
        create_account()
    else:
        print(Fore.RED+"Invalid input")
        start()


def train_chart():
    cur.execute("select * from trains")
    flag=True
    print(Fore.YELLOW+"{:13}{:13}".format("Train No.","Train Route"))
    print()
    while flag==True:
        try:
            a=cur.fetchone()
            b=eval(a[1])
            print("{:<12}".format(a[0]),end=' ')
            print(b[0], end="")
            i=1
            while True:
                print('-->', b[i],end=' ')
                i+=1
        except IndexError:
            pass
        except:
            flag=False
        print()


def menu():
    print(Fore.BLUE+"="*35+"MENU"+"="*38)

    print("Press "+Fore.YELLOW+ "a"+" to log into another account/create a new account")
    print("Press "+Fore.YELLOW+ "b"+" to book tickets")
    print("Press "+Fore.YELLOW+ "c"+" to cancel tickets")
    print("Press "+Fore.YELLOW+ "d"+" to view your profile")
    print("Press "+Fore.YELLOW+ "e"+" to view the train routes")
    print("Press "+Fore.YELLOW+ "f"+" to exit the program")
    print(Fore.BLUE+"="*77)
    print(Fore.MAGENTA+"Enter your choice: ", end=" ")
    x=input()
    print(Fore.BLUE+"="*77)

    if x in ['a','A']:
        start()
    elif x in ['b','B']:
        booking()
        menu()
    elif x in ['c','C']:
        cancel()
        menu()
    elif x in ['d','D']:
        profile()
        menu()
    elif x in ['e','E']:
        train_chart()
        menu()
    elif x in ['f','F']:
        print("Thank you for choosing us.")
        return
    else:
        print(Fore.RED+"Invalid input")
        print(Fore.RED+"Please enter a valid option")
        menu()


def profile():
    global u
    temp=str('select * from '+u)
    cur.execute(temp)
    a=cur.fetchall()
    temp=str('select * from account where username="'+u+'"')
    cur.execute(temp)
    b=cur.fetchone()
    print(Fore.BLUE+"="*36+"PROFILE"+"="*34)
    print(Fore.CYAN+"Username\t: ",b[0])
    print(Fore.CYAN+"Name\t\t: ",b[2])
    print(Fore.CYAN+"Age\t\t: ",b[3])
    print(Fore.CYAN+"Phone no.\t: ",b[4])
    print(Fore.CYAN+"Balance\t\t: ",b[5])
    print(Fore.CYAN+"Ticket details: ")
    print()
    print(Fore.YELLOW+"{:15} {:15} {:15}".format("TRAIN NO.","SEATS","STATUS"))
    if len(a)!=0:
        for i in a:
            print(Fore.CYAN+"{:<15} {:<15} {:<15}".format(i[0],i[1],i[2]))
    else:
        print("  NO TICKETS BOOKED YET")
    print(Fore.BLUE+"="*77)
    return


def cancel():
    global u
    try:
        print(Fore.RED+"WARNING:All booked or waitlisted tickets on given train will be cancelled \
\nand 10% cancellation fee will apply")
        print(Fore.RED+"Please confirm your identity")
        p=input("Enter password:")
        temp=("select * from account where username='"+u+"'")
        cur.execute(temp)
        a=cur.fetchone()      
        if a[1]==p:
            print(Fore.GREEN+"Identity verified")
        else:
            print(Fore.RED+"Invalid Credentials")
            print(Fore.RED+"Returning to Main Menu")
            return
        train_chart()
        b=int(input("Enter train number to cancel tickets:"))
        cur.execute(str("select * from "+u))
        c=cur.fetchall()
        flag=0
        seats=0
        for i in c:
            if i[0]==b and i[2]=='Booked':
                flag=1
                d=i[1]
                cur.execute(str("update "+u+" set status='Cancelled' where train_no="+str(b)+" and status='Booked'"))
                con.commit()
                try:
                    cur.execute(str("select * from "+u+" where train_no="+str(b)+" and status='Waitlisted'"))
                    temp=cur.fetchall()[0]
                    cur.execute(str("delete from "+u+" where train_no="+str(b)+" and status='Waitlisted'"))
                    con.commit()
                    cur.execute(str("update "+u+" set seats="+str(d+temp[1])+" where train_no="+str(b)))
                except:
                    pass
                try:
                    seats+=d+temp[1]
                except:
                    seats+=d
                cur.execute("select * from available where train_no=%s"%(b,))
                x=cur.fetchone()
                if x[1]<0:
                    cur.execute("select * from waitlist where train_no=%s"%(b,))
                    y=cur.fetchall()
                    for z in y:
                        if d==0:
                            break
                        if z[1]>d and d>0:
                            cur.execute("select * from %s where status='Booked' and train_no=%s"%(z[2],b))
                            temp=cur.fetchone()
                            e=d+temp[1]
                            cur.execute("update %s set seats=%s where status='Booked' and train_no=%s"%(z[2],e,b))
                            cur.execute("update %s set seats=%s where status='Waitlisted' and train_no=%s"%(z[2],z[1]-d,b))
                            cur.execute("update waitlist set seats=%s where train_no=%s and username='%s'"%(z[1]-d,b,z[2]))
                            con.commit()
                            d=0
                        if z[1]<=d:
                            cur.execute("delete from %s where train_no=%s and status='Waitlisted'"%(z[2],b))
                            try:
                                cur.execute("select * from %s where status='Booked' and train_no=%s"%(z[2],b))
                                temp=cur.fetchall()[0]
                                e=z[1]+temp[1]
                            except:
                                e=z[1]
                            cur.execute("update %s set seats=%s where train_no=%s and status='Booked'"%(z[2],e,b))
                            cur.execute("delete from waitlist where train_no=%s and username='%s'"%(b,z[2]))
                            con.commit()
                            d-=z[1]
                    if d>0:
                        cur.execute("select * from available where train_no=%s"%(b,))
                        e=d+cur.fetchall()[0][1]
                        cur.execute("update available set seats=%s where train_no=%s"%(e,b))
                        con.commit()
                else:
                    try:
                        cur.execute("select * from available where train_no=%s"%(b,))
                        e=d+cur.fetchall()[0][1]
                    except:
                        e=d
                    cur.execute("update available set seats=%s where train_no=%s"%(e,b))
                    con.commit()
        else:
            for i in c:
                if i[0]==b and i[2]=='Waitlisted':
                    cur.execute("delete from waitlist where train_no=%s and username='%s'"%(b,u))
                    cur.execute("delete from %s where train_no=%s and status='Waitlisted'"%(u,b))
                    con.commit()
        if flag==0:
            print(Fore.RED+"No tickets found")
        else:
            print(Fore.GREEN+"Tickets cancelled successfully")
            cur.execute("select * from available")
            pricing=cur.fetchall()[0][4]
            print(Fore.GREEN+"Amount to be refunded: "+str((pricing*seats)*0.9))
            cur.execute("update account set balance=balance-%s where username='%s'"%((pricing*seats)*0.9,u))
            con.commit()
    except:
        print(Fore.RED+"--------------------------")
        print(Fore.RED+"|     ERROR OCCURED      |")
        print(Fore.RED+"| RETURNING TO MAIN MENU |")
        print(Fore.RED+"--------------------------")
        return


#MAIN PROGRAM
text="Welcome to Railway Registration and Management System"
slowprint(text)
start()
end=input()