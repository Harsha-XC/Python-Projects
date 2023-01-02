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
    cur.execute('create table accounts(username varchar(100) primary key,password varchar(100))')
    cur.execute('create table blocked(from_user varchar(100),to_user varchar(100))')

#Defining functions
def login_screen():
    global login
    login=False
    def getvalues():
        global login
        m=a.get()
        n=b.get()
        cur.execute('select * from accounts')
        x=cur.fetchall()
        for i in x:
            if i[0]==m:
                if i[1]==n:
                    login=True
                else:
                    window.destroy()
                    login_screen()
    window=Tk()
    window.geometry('300x150')
    window.title('Login')
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

def intro_page():
    def to_login():
        window.destroy()
        login_screen()

    def to_create():
        window.destroy()
        create_screen()

    window=Tk()
    window.geometry('300x150')
    window.title('ECS')
    window.resizable(False,False)

    l=Label(window,text='Please select an option')
    l.pack(pady=10)

    b1=Button(window,text='Log into an existing account',command=to_login)
    b1.pack(pady=10)

    b2=Button(window,text='Create a new account',command=to_create)
    b2.pack(pady=10)
    window.mainloop()

def create_screen():
    window=Tk()
    window.geometry('300x700')
    window.title('Create an account')
    window.resizable(False,False)

    
#Main Program
intro_page()
