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
    cur.execute('use rrms')
    cur.execute('create table accounts(username varchar(100) primary key,password varchar(100))')
    cur.execute('create table blocked(from_user varchar(100),to_user varchar(100))')

#Defining functions
def login_screen():
    def getvalues():
        global msg,login
        m=a.get()
        n=b.get()
        cur.execute('select * from accounts')
        x=cur.fetchall()
        for i in x:
            if i[0]==m:
                if i[1]==n:
                    login=True
                else:
                    msg='Incorrect Password'
        else:
            msg='User not found'
    window=Tk()
    window.geometry('300x200')
    window.title()
    window.resizable(False,False)

    c1=Canvas(window)
    c1.pack()
    x=Label(c1,text='Username:')
    x.pack(side=LEFT)
    a=Entry(c1)
    a.pack(side=RIGHT)

    c2=Canvas(window)
    c2.pack()
    y=Label(c2,text='Password: ')
    y.pack(side=LEFT)
    b=Entry(c2)
    b.pack(side=RIGHT)

    but=Button(window,command=getvalues,text='Submit')
    but.pack()

    l=Label(window,text=msg)
    l.pack()
    window.mainloop()

#Main Program
msg=''
login=False
login_screen()