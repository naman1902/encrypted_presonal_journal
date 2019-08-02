import datetime;
import sys;
from cryptography.fernet import Fernet
from collections import OrderedDict

def binaryTostring(key):
    h=key.decode()
    return h
def stringTobinary(key):
    h=key.encode()
    return h

def getrecord(f1):
    dict_record=OrderedDict()
    f1.seek(0,0)
    g=f1.readline()
    g=stringTobinary(g)
    fernet1=Fernet(g)
    f2=f1.readlines()
    count1=0
    for x in f2:
        if count1%2 == 0:
            un=x[:-1]
            un=stringTobinary(un)
            un=fernet1.decrypt(un)
            un=binaryTostring(un)
            count1+=1
            
        else:
            pwd=x[:-1]
            pwd=stringTobinary(pwd)
            pwd=fernet1.decrypt(pwd)
            pwd=binaryTostring(pwd)
            dict_record[un]=pwd
            count1+=1
    return dict_record

    
def createEntry(filename):
    f1=open(filename+".txt","r+")
    f1.seek(0,0)
    g=f1.readline()
    g=stringTobinary(g[:-1])
    fernet1=Fernet(g)
    f1.seek(0,0)
    dict_records=getrecord(f1)
    l=list(dict_records.keys())
    ts = datetime.datetime.now()
    ts=ts.strftime("%d %b, %Y %I:%M:%S%p")
    print(ts,end=": ")
    story=input()
    if len(dict_records)==50:
        dict_records.pop(l[0])
        dict_records[ts]=story
        f1=open(filename+".txt","w")
        g=binaryTostring(g)+"\n"
        f1.write(g)
        for x in dict_records:
            reco=dict_records[x]
            x=stringTobinary(x)
            x=fernet1.encrypt(x)
            x=binaryTostring(x)
            f1.write(x+"\n")
            reco=stringTobinary(reco)
            reco=fernet1.encrypt(reco)
            reco=binaryTostring(reco)
            f1.write(reco+"\n")
        f1.close()
    else :
        f1.seek(0,2)
        ts=stringTobinary(ts)
        ts=fernet1.encrypt(ts)
        ts=binaryTostring(ts)
        ts=ts+"\n"
        story=stringTobinary(story)
        story=fernet1.encrypt(story)
        story=binaryTostring(story)
        story=story+"\n"
        f1.write(ts)
        f1.write(story)
        f1.close()
    menu2(filename)
    
    
def viewEntry(filename):
    f1=open(filename+".txt","r+")
    dict_records=getrecord(f1)
    m=list(dict_records.keys())
    print (m)
    for x in m:
        print(x,end=": ")
        print(dict_records[x])
    f1.close()
    menu2(filename)
    
def menu2(filename):
    print("1: create Entry          2: View Entries          3: Logout\n")
    i=input()
    if i=='1' :
        createEntry(filename)
    elif i=='2' :
        viewEntry(filename)
    elif i=='3' :
        print("######### logged out ##########")
        global q
        menu(q)
    else:
        print("Invalid input")
        menu2(filename)

def signin(q):
    file=open(q+".txt","r+")
    if(len(users)==10):
        print("Max User Capacity reached")
        menu(q)
    else:
        uname=input("Username: ")
        pword=input("Password: ")
        try:
            f1=open(uname+".txt","r+")
            print("username already exist")
            f1.close()
            menu(q)
        except:
            users[uname]=pword
            f1=open(uname+".txt","a")
            key=Fernet.generate_key()
            key=binaryTostring(key)+"\n"
            f1.write(key)
            f1.close()
            global fernet
            uname1=uname+""
            uname=stringTobinary(uname)
            uname=fernet.encrypt(uname)
            uname=binaryTostring(uname)
            uname=uname+"\n";
            pword=stringTobinary(pword)
            pword=fernet.encrypt(pword)
            pword=binaryTostring(pword)
            pword=pword+"\n";
            file.seek(0,2)
            file.write(uname)
            file.write(pword)
            file.close()
            global count
            count=count+1
            menu2(uname1)
    
def login(q):
    uname=input("Username: ")
    pword=input("Password: ")
    try:
        if (pword==users[uname]):
            print("########### Logged in. Welcome "+uname+" ##############")
            menu2(uname)
        else:
            print("Invalid Credentials")
            menu(q)
    except:
        print("Invalid Credentials")
        menu(q)
        

def menu(q):
    print("1: login            2: Signin             3:Exit\n")
    n=int(input())
    if(n==1):
        login(q)
    elif(n==2):
        signin(q)
    elif(n==3):
        sys.exit()
    else:
        print("Invalid input")
        menu(file)

users={}
q="users"
try:
    file=open(q+".txt","r+")
except:
    file=open(q+".txt","a")
    key1=Fernet.generate_key()
    key1=binaryTostring(key1)+"\n"
    file.write(key1)
    file.close()
file=open(q+".txt","r+")
file.seek(0,0)
key1=file.readline()
key1=stringTobinary(key1[:-1])
fernet=Fernet(key1)
f=file.readlines()
count=0
for x in f:
    if count%2 == 0:
        un=x[:-1]
        un=stringTobinary(un)
        un=fernet.decrypt(un)
        un=binaryTostring(un)
        count+=1
    else:
        pwd=x[:-1]
        pwd=stringTobinary(pwd)
        pwd=fernet.decrypt(pwd)
        pwd=binaryTostring(pwd)
        users[un]=pwd
        count+=1
count/=2
file.close()
menu(q)

