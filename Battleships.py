from random import randint
b=[]
for i in range(5):
    b.append([0]*5)
def print_board(b):
    for i in range(len(b)):
        for j in range(len(b)):
            print(" ",b[i][j],end='')
        print()
def random_row(b):
    return randint(0,len(b)-1)
def random_col(b):
    return randint(0,len(b)-1)
d=[[],[]]
l=[]
for i in range(2):
    x=random_row(b)
    y=random_col(b)
    d[0]+=[x]
    d[1]+=[y]
    l+=[[x,y]]
for i in l:
    while l.count(i)>1: 
        x=random_row
        y=random_row
        a=[x,y]
        l.remove(i)
        l+=[a]
b_ship=5
print("BATTLESHIPS!")
print("You will have 10 turns to find the battleship")
print("0 : Empty spot")
print("X : Miss")
print("* : Battleship Sunk")
print_board(b)
turn=1
while turn<=10:
    print("Turn",turn)
    try:
        guess_row = int(input("Guess Row:"))-1
        guess_col = int(input("Guess Coloumn:"))-1
    except:
        print("Please enter a valid input")
        continue
    if guess_row>4 or guess_col>4 or guess_row<0 or guess_col<0:
        print("OUT OF THE MAP! FILL IN THE COORDINATES ACCURATELY")
        if turn==11:
            print("GAME OVER!")
    elif b[guess_row][guess_col]=='X'or b[guess_row][guess_col]=='*':
        print("You've already tried that. Try something else")
        if turn==11:
            print("GAME OVER!")
    elif guess_row in d[0] and guess_col in d[1]:
        if [guess_row,guess_col] in l:
            print("BATTLESHIP SUNK!")
            b_ship-=1
            b[guess_row][guess_col]='*'
            turn+=1
        else:
            print("TARGET MISSED!")
            b[guess_row][guess_col]='X'
            turn+=1
        if turn==11:
            print("GAME OVER!")
    else:
        print("TARGET MISSED!")
        b[guess_row][guess_col]='X'
        turn+=1
        if turn==11:
            print("GAME OVER!")
    print_board(b)
    if b_ship==0:
        print("CONGRATULATIONS! YOU WON!")
        break
input("\n\nPRESS ENTER TO EXIT")
print("Thank you for playing")
print("MADE BY:")
print("Adithi Ambatipudi (11A)")
print("Harsha Vishwanath (11A)")