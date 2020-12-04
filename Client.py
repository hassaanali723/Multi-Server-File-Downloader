#PROJECT NAME : MULTI SERVER FILE DOWNLOADER
#GROUP MEMBERS : HASSAAN ALI MEHMOOD
#                MAMNOON UL HUSSNAIN


#THIS PROGRAM WILL HANDLE CLIENT SIDE
#CLIENT WILL CONNECT WITH MULTIPLE SERVERS IN MULTIPLE THREADS , COLLECTS SEGMENTS FROM DIFFERENT SERVERS
#AND COMBINE THEM IN ORDER , IT HAS LOAD BALANCING AND RESUME FUNCTIONALITY

import socket
import threading
import time


HEADER=64
host=socket.gethostbyname(socket.gethostname())
portslist=[]
liveServers=[]
deadServers=[]
filesegments = [0]*4  # we are initializing it by 4 , but this will change after getting input from the user (by making it global)
downloadedbytes=[0]*4
downloadedSpeed=[0]*4
totalBytes=[0]*4
thread=[]
totalsegments=[]
recievedsegments=[]
file_size=0
file_location=None
resume=False
data=0
totalserver=[]

#function to connect with servers in parallel
def server_start(portslist,y):

 try:
    s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # s1.bind((host,portslist[y]))
    s1.connect((host, portslist))
    a=s1.getsockname()
    liveServers.append(portslist)
    time.sleep(0.5)
    sendmsg(s1,y)
    file_receive(s1,filesegments,y)

 except:
    print(f"Server {y+1} did not respond")

#function to send segment no to server
def sendmsg(s1,x):

    msg=str(x)
    message = msg.encode("utf-8")
    msg_length = len(message)
    send_length = str(msg_length).encode("utf-8")
    send_length += b' ' * (HEADER - len(send_length))
    s1.send(send_length)
    s1.send(message)

#function to receive segment from server
def file_receive(s1,filesegments,y):

            global file_size
            file_size = s1.recv(6).decode("utf-8")
            start=time.time()
            time.sleep(0.0000000001)
            server1data = s1.recv(200000)
            downloadedbytes[y]=len(server1data)
            totalBytes[y] = len(server1data)
            end=time.time()
            speed=(len(server1data)*0.001)/(end-start)
            downloadedSpeed[y]=round(speed)
            filesegments[y]=server1data
            file=open("segmentsData.txt",'ab')
            data=server1data
            file.write(data)
            file.write(b'lol')    #writing extra string into a file , so that we can split by using this string
            file1=open("segments.txt",'a')
            seg_no=str(y)+"se"    #writing extra string into a file , so that we can split by using this string
            file1.write(seg_no)
            recievedsegments.append(y)
            byt=open("downloadedBytes.txt",'a')
            byt.write(str(len(server1data))+"se")
            sp=open("speed.txt",'a')
            sp.write(str(round(speed))+"se")  #writing extra string into a file , so that we can split by using this string


#function to receive file size from server
def fileSizeRecv(s1):

    msg_length = s1.recv(2048).decode("utf-8")
    msg_length = int(msg_length)




# function to show status on screen

def show_status(downloadedbytes,totalBytes,downloadedSpeed):
    for i in range(len(portslist)):
        print(f"Server {i+1} : Downloaded Bytes-{downloadedbytes[i]} / Total Bytes-{totalBytes[i]} , Download Speed : {downloadedSpeed[i]} kb/s")
    print(f"Total : {sum(downloadedbytes)} / {file_size} , Download Speed :{round(sum(downloadedSpeed)/len(downloadedSpeed))} kb/s")



#function for laod balancing
def remaining_segments():

        remaining_segments=list(set(totalsegments) - set(recievedsegments))
        if len(remaining_segments)>0 :

         for z in range(len(remaining_segments)):
            portNo=liveServers[0]
            segmentNO=remaining_segments[z]
            server_start(portNo,segmentNO)
            byt=downloadedbytes[segmentNO]
            downloadedbytes[recievedsegments[0]]+=byt
            totalBytes[recievedsegments[0]]+=byt
            downloadedbytes[segmentNO]=0
            downloadedSpeed[segmentNO]=0



#function to write on a file after receiving  all the segments
def write_file(filesegments,file_location):

    if len(liveServers) == len(portslist) or resume==True  :

        file = open(file_location, 'wb')
        for s in range(len(filesegments)):

            file.write(bytes(filesegments[s]))


# function the show the output according to the time specified by the user in separate thread
def status(ti):
    while True:
        time.sleep(ti)
        show_status(downloadedbytes, totalBytes, downloadedSpeed)


# The very first function of the program that will run and ask for the no of servers that the user want to create.
def start():

 var=int(input("To How many servers you want to connect...?"))
 global filesegments
 global downloadedSpeed
 global downloadedbytes
 global totalBytes
 filesegments=[0]*var
 downloadedbytes=[0]*var
 totalBytes=[0]*var
 downloadedSpeed=[0]*var
 return var


# function that will ask for the port list
def ports_lst(var):

 for x in  range(var):
    ports = int(input(f"PLease enter the port no of server {x + 1} :"))
    portslist.insert(x, ports)
    totalserver.append(ports)
    totalsegments.append(x)

# function that will ask for the time interval
def timer():
    t=int(input("Enter the time interval (seconds) between metric reporting :"))
    return t


# function that will ask for the location of output directory
def file_loc():
    ip=input(str("Enter the IP Address of Server :"))
    fi=input(str("Enter the location of output directory :"))
    global file_location
    file_location=fi


#function to conncet with the servers in threads
def connect():

 for y in range(len(portslist)):


    thread.append(threading.Thread(target=server_start, args=(portslist[y],y)))
    thread[y].start()
    time.sleep(0.1)



# function to handle resume downloading
def resume():
    res=input(str("Would like to continue download progress ? Press r :"))
    if res=="r":
        global resume
        resume=True

        d=open("downloadedBytes.txt",'r')
        da=d.read()
        dat=da.split("se")

        s=open("speed.txt",'r')
        sp=s.read()
        splist=sp.split("se")

        file2=open("Segments.txt",'r')
        seg=file2.read()
        seg_list=seg.split("se")

        file3=open("segmentsData.txt",'rb')
        data=file3.read()
        datalst=data.split(b"lol")

        for i in range(len(seg_list)-1):
            p=int(seg_list[i])
            recievedsegments.append(p)
            filesegments[p]=datalst[i]
            downloadedbytes[p]=int(dat[i])
            totalBytes[p]=int(dat[i])
            downloadedSpeed[p]=int(splist[i])

        remaining_segments = list(set(totalsegments) - set(recievedsegments))

        for z in range(len(remaining_segments)):
            portNo=portslist[z]
            segmentNO=remaining_segments[z]
            thread.append(threading.Thread(target=server_start,args=(portNo,segmentNO)))
            thread[z].start()

        for i in range(len(remaining_segments)):
            thread[i].join()

    else :                                  # In case when we dont want to resume the downloading
        f1 = open("segments.txt", 'w')
        f2 = open("segmentsData.txt", 'wb')
        d1=open("downloadedBytes.txt",'w')
        s1=open("speed.txt",'w')
        connect()
        for i in range(len(portslist)):
            thread[i].join()




# Function calls

var=start()
file_loc()
ti=timer()
ports_lst(var)
resume()
thr=threading.Thread(target=status,args=(ti,))
thr.start()
remaining_segments()
time.sleep(5)
write_file(filesegments,file_location)

