from random import randint
str = ""
print("_____________________________________")
print("*          가위바위보 게임            *")
count = 0
while(count<3):
    com  = randint(1,3)
    pl = int(input("가위:1  바위:2  보:3 중 하나를 내세요:"))
    print("com:%d   player:%d"%(com,pl))
    if(com%3+1==pl):
        print("player Win") 
        break
    elif(pl%3+1==com):print("computer Win")
    else: print("Draw!")
    count+=1
print("*                 종료               *")
print("_____________________________________")
