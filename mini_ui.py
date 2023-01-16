#E-Communication System (ECS)

#Importing modules
from tkinter import *
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
    global u 
    def getvalues():
        global u
        m=a.get()
        n=b.get()
        cur.execute('select * from accounts')
        x=cur.fetchall()
        for i in x:
            if i[0]==m:
                if i[1]==n:
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
            cur.execute("insert into accounts values('%s','%s','%s','%s')"%(a1,a2,a3,str(a4)))
            cur.execute("create table %s(from_user varchar(100),message varchar(500))"%(a1,))
            con.commit()
            u=a1
            window.destroy()
            mainmenu()
        except:
            msg='Unavailable Username'
            window.destroy()
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

def mainmenu(msg=''):
    def exitpls():
        window.destroy()
    def to_send():
        window.destroy()
        send()
    def to_block():
        window.destroy()
        block()
    def to_inbox():
        window.destroy()
        #inbox()
    def to_unblock():
        window.destroy()
        #unblock()
    def to_profile():
        window.destroy()
        #profile()
    window=Tk()
    window.geometry('300x380')
    window.title('ECS')
    window.resizable(False,False)

    l=Label(window,text='MAIN MENU')
    l.pack()

    l2=Label(window,text=msg)
    l2.pack()

    b1=Button(window,text='Change account',command=intro_page)
    b1.pack(pady=10)   

    b7=Button(window,text='Open your inbox',command=to_inbox)
    b7.pack(pady=10)

    b2=Button(window,text='Send a message',command=to_send)
    b2.pack(pady=10) 

    b3=Button(window,text='Block a user',command=to_block)
    b3.pack(pady=10) 

    b4=Button(window,text='Pardon a user',command=to_unblock)
    b4.pack(pady=10) 

    b5=Button(window,text='View your profile',command=to_profile)
    b5.pack(pady=10) 

    b6=Button(window,text='Exit',command=exitpls)
    b6.pack(pady=10) 
    window.mainloop()

def send(msg=''):
    def sendmsg():
        global u
        m=e.get()
        n=a.get()
        window.destroy()
        if m!='':
            cur.execute("select * from blocked where from_user='%s' and to_user='%s'")
            x=cur.fetchall()
            if x!=[]:
                cur.execute("insert into %s values(%s,%s)"%(n,u,m))
            else:
                send('User was blocked')
        else:
            send("No username entered")
    def back():
        window.destroy()
        mainmenu('Message sent')
    window=Tk()
    window.geometry('300x300')
    window.title('ECS')
    window.resizable(False,False)

    l1=Label(window,text='SEND A MESSAGE')
    l1.pack()

    l2=Label(window,text=msg)
    l2.pack(pady=10)

    c1=Canvas(window)
    c1.pack(pady=10)
    x=Label(c1,text='To:')
    x.pack(side=LEFT)
    a=Entry(c1)
    a.pack(side=RIGHT)

    y=Label(window,text='Message: ')
    y.pack(pady=10)

    e=Entry(window)
    e.pack(pady=5)

    b=Button(window,text='Send',command=sendmsg)
    b.pack(pady=10)

    b1=Button(window,text='Back',command=back())
    b1.pack(pady=10)
    window.mainloop()
def block(msg=''):
    def menupls():
        window.destroy()
        mainmenu()
    def sendinfo():
        global u
        window.destroy()
        x=e.get().strip()
        if x=='':
            block('Enter valid input')
        else:
            cur.execute("select * from accounts")
            a=cur.fetchall()
            for i in a:
                if i[0]==x:
                    cur.execute("insert into blocked values('%s','%s')"%(u,x))
                    con.commit()
                    flag=True
            if not flag:
                block('User not found')
            else:
                mainmenu('User successfully blocked')
    window=Tk()
    window.geometry('300x250')
    window.title('ECS')
    window.resizable(False,False)

    l3=Label(window,text='BLOCK A USER')
    l3.pack()

    l2=Label(window,text=msg)
    l2.pack(pady=10)

    l=Label(window,text='Enter the name of user to be blocked:')
    l.pack(pady=10)

    e=Entry(window)
    e.pack(pady=5)

    b1=Button(window,text='Submit',command=sendinfo)
    b1.pack(pady=10)

    b2=Button(window,text='Back',command=menupls)
    b2.pack(pady=10)

    window.mainloop()
#Main Program
intro_page()