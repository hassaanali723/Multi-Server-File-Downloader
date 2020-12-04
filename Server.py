#PROJECT NAME : MULTI SERVER FILE DOWNLOADER
#GROUP MEMBERS : HASSAAN ALI MEHMOOD
#                MAMNOON UL HUSSNAIN

#PROGRAM THAT WILL HANDLE SERVER SIDE .
# THIS PROGRAM WILL CREATE MULTIPLE SERVERS IN MULTIPLE THREADS AS THE USER SPECIFIED
# AND WILL CREATE THE CHUNKS OF FILE FOR EACH SERVER . WHEN THE SERVER RECEIVES THE MSG FROM THE CLIENT SIDE ,
# SERVER WILL SEND THE SPECIFIC SEGMENT OF THAT FILE TO THE CLIENT SPECIFIED IN THE MESSAGE BY THE CLIENT


import socket
import threading
import time

DISCONNECT_MESSAGE="end"
host=socket.gethostname()
HEADER=64
portslist=[]   # port list for all the servers
segmentlist=[]  # segments of file
count=0
sockets=[]    #list for sockets in order to close the server
closed_servers=[]
statuslist=[]  #To maintain the record of server status
file_loc=None
No_of_Servers=None


# function to create servers and file segmentation
def server(portslist,y,var,file_loc):
  try:
    s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sockets.append(s1)
    s1.bind((host, portslist))
    s1.listen()
    statuslist.append("Alive")
    file = open(file_loc, 'rb')
    chunk=file.read(500000)
    file.close()
    length=len(chunk)
    file_size=length
    c, d = divmod(length, var)
    file = open(file_loc, 'rb')
    for i in range(var - 1):
        length = 1 * c

        segmentlist.append(file.read(length))

    length=c+d
    segmentlist.append(file.read(length))
    file.close()

    while True:
        conn, addr = s1.accept()
        send_file(conn,addr,segmentlist,file_size)

  except:
      closed_servers.append(s1)



# This function will handle the message send by client and send the file chunk accordingly
def send_file(conn,addr,segmentlist,file_size):

        msg_length=conn.recv(HEADER).decode("utf-8")
        if msg_length:
         msg_length=int(msg_length)
         msg=conn.recv(msg_length).decode("utf-8")

        try:
           msg1=int(msg)
           fil = str(file_size)
           filesize = fil.encode("utf-8")
           conn.send(filesize)
           conn.send(segmentlist[msg1])

        except:
         print("failed")


# This function will send the file size to the client
def fileSize(conn,addr,file_size):
    fil = str(file_size)
    message = fil.encode("utf-8")
    conn.send(message)


#This function will give the details of status
def status(portslist,statuslist):

 for z in range(len(portslist)):
    print(f"Server :{z+1} , Port No :{portslist[z]} , Status : {statuslist[z]} , Press e{z+1} to off Server {z+1} / Press o{z+1} to on Server {z+1} ..")


#This function will take input from console, close the server and reconnect with the server
def server_close(portslist,var,file_loc):

 while True:

    of = input(str())
    b=of.split('e')
    # o=of.split('o')
    if b[0]=='':
     c=b[1]
     d=int(c)
     sockets[d-1].close()
     statuslist[d-1]="Dead"
     status(portslist,statuslist)

    else :
        o = of.split('o')
        l = o[1]
        m = int(l)
        p=portslist[m-1]
        y=m-1
        statuslist[m - 1] = "Alive"
        thre=threading.Thread(target=server , args=(p,y,var,file_loc))
        thre.start()
        status(portslist, statuslist)

# This function will report the output according to the time interval specified by the user
def report(ref_time):
    while True:
        time.sleep(ref_time)
        status(portslist, statuslist)


# This function will take all the inputs from console , No of servers,ports list,file location,time interval
def start():

 var=int(input("How many servers you want to create...?"))
 ti=int(input("Enter the time interval (seconds) between server status reporting :"))
 fi=input(str("Enter the Location of file :"))
 global No_of_Servers
 No_of_Servers=var
 global file_loc
 file_loc=fi
 for x in  range(var):
    ports = int(input(f"PLease enter the port no for server {x + 1} :"))
    portslist.insert(x, ports)



 for y in range(len(portslist)):


    thread = threading.Thread(target=server, args=(portslist[y],y,var,file_loc))
    thread.start()


 return ti



#Function calls

ref_time=start()
time.sleep(1.2)
thread=threading.Thread(target=report,args=(ref_time,)) # Separate thread for output status reporting
thread.start()
server_close(portslist,No_of_Servers,file_loc) # To handle the command of closing and reconnecting with the server






