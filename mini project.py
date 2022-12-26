#Importing modules
import pickle
import colorama

#Defining functions
def create_file():
    try:
        f=open("miniproject.dat",'r')
        f.close()
        mainmenu()
    except:
        f=open('miniproject.dat','w')
        f.close()
        create_file()

def mainmenu():
    print("Press 1 to read the wall of comments")
    print("Press 2 to write a new anonymous message")
    print("Press 3 to exit program")
    x=int(input("Choice:"))
    if x==1:
        read()
        menu()
    elif x==2:
        write()
        menu()
    elif x==3:
        print("Thank you")
    else:
        print("Please enter valid input")
        menu()

def read():
    f=open('miniproject.dat')
    a=pickle.load(f)
    for i in a: 
        print(i)
    menu()

def write():
    x=input("Enter anonymous message:")
    