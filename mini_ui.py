#E-Communication System (ECS)

#Importing modules
from tkinter import *
from PIL import ImageTk, Image
import mysql.connector as sql

#Setting up MySQL
con=sql.connect(user='root',host='localhost',password='sql123')
cur=con.cursor()
try:
    cur.execute('use mini')
except:
    cur.execute('create database mini')
    cur.execute('use mini')
    cur.execute('create table accounts(username varchar(100) primary key,password varchar(100),full_name varchar(100),phone_no varchar(20))')
    cur.execute('create table blocked(from_user varchar(100),to_user varchar(100))')

#Defining functions
def login_screen():
    global login,u 
    login=False
    def getvalues():
        global login,u
        m=a.get()
        n=b.get()
        cur.execute('select * from accounts')
        x=cur.fetchall()
        for i in x:
            if i[0]==m:
                if i[1]==n:
                    login=True
                    u=m
                    window.destroy()
                    mainmenu()
                else:
                    window.destroy()
                    msg='Incorrect password'
                    intro_page(msg)
        else:
            window.destroy()
            msg='Incorrect username'
            intro_page(msg)
    window=Tk()
    window.geometry('300x170')
    window.title('ECS')
    window.resizable(False,False)

    c1=Canvas(window)
    c1.pack(pady=10)
    x=Label(c1,text='Username:')
    x.pack(side=LEFT)
    a=Entry(c1)
    a.pack(side=RIGHT)

    c2=Canvas(window)
    c2.pack(pady=10)
    y=Label(c2,text='Password: ')
    y.pack(side=LEFT)
    b=Entry(c2)
    b.pack(side=RIGHT)

    but=Button(window,command=getvalues,text='Submit')
    but.pack(pady=10)

    window.mainloop()

def intro_page(msg='Welcome!'):
    def to_login():
        window.destroy()
        login_screen()

    def to_create():
        window.destroy()
        create_screen()

    window=Tk()
    window.geometry('300x200')
    window.title('ECS')
    window.resizable(False,False)

    msg_l=Label(window,text=msg)
    msg_l.pack(pady=10)

    l=Label(window,text='Please select an option')
    l.pack(pady=10)

    b1=Button(window,text='Log into an existing account',command=to_login)
    b1.pack(pady=10)

    b2=Button(window,text='Create a new account',command=to_create)
    b2.pack(pady=10)

    window.mainloop()

def create_screen():
    def exec_acc():
        global u
        a1,a2,a3,a4=b.get(),y.get(),n.get(),q.get()
        try:
            cur.execute('''insert into accounts values('%s','%s','%s','%s')'''%(a1,a2,a3,a4))
            window.destroy()
            mainmenu()
            u=a1
        except:
            msg='Unavailable Username'
            intro_page(msg)
    window=Tk()
    window.geometry('300x250')
    window.title('ECS')
    window.resizable(False,False)

    c1=Canvas(window)
    c1.pack(pady=10)
    a=Label(c1,text='Username: ')
    a.pack(side=LEFT)
    b=Entry(c1)
    b.pack(side=RIGHT)

    c2=Canvas(window)
    c2.pack(pady=10)
    x=Label(c2,text='Password: ')
    x.pack(side=LEFT)
    y=Entry(c2)
    y.pack(side=RIGHT)

    c3=Canvas(window)
    c3.pack(pady=10)
    m=Label(c3,text='Full Name: ')
    m.pack(side=LEFT)
    n=Entry(c3)
    n.pack(side=RIGHT)

    c4=Canvas(window)
    c4.pack(pady=10)
    p=Label(c4,text='Phone number: ')
    p.pack(side=LEFT)
    q=Entry(c4)
    q.pack(side=RIGHT)

    b1=Button(window,text='Create account',command=exec_acc)
    b1.pack(pady=10)   

    window.mainloop()

def mainmenu():
    window=Tk()
    window.geometry('300x250')
    window.title('ECS')
    window.resizable(False,False)

    b1=Button(window,text='Change account',command=intro_page)
    b1.pack(pady=10)   

    b1=Button(window,text='Send a message',command=send)
    b1.pack(pady=10) 

    b1=Button(window,text='',command=block)
    b1.pack(pady=10) 

    b1=Button(window,text='Create account',command=unblock)
    b1.pack(pady=10) 
#Main Program
intro_page()
