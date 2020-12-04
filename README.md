# Multi-Server-File-Downloader

Abstract:

Firstly, we would like to tell what the importance is of doing this project. This project was designed so we can practically implement the things that we have learned earlier in the “Computer Networks” course. Basically, we have programmed a downloader based on the client-server communication method. The additional thing in this project is that we have a single client and multiple servers offering the chunks of a video file. The things learned during this project have been a great addition to our knowledge and problem-solving skills. After finishing this project, we have a vast knowledge of socket programming and we are confident of making sometmething on a much greater scale later. The main problem faced during this project was to make multiple servers. Although there is vast information on the internet about making multiple client system but not about multiple server system. Overall, it was a totally new experience of working in a two membered team and we realized the importance of an enhanced communication because earlier we were doing projects in a four membered team and it was a challenging thing too. 

Methodology:

The basis of this project is socket programming. The client server communication starts by invoking a TCP connection.The main idea is to utilize threading to create multiple servers that run parallelly with a single client,and we have used the threading methods(i.e join) to maintain the timing of different functionalities . The file is divided into chunks equal to the number of servers created by the user. Each server has got all the chunks of the video file and available for the client to download the chunks of data. The feature of load balancing is also available. If the size of the downloaded chunks is not equal to the whole size of the video file, then load balancing is done and the remaining chunks are obtained from the live servers. After receiving all the chunks of the file successfully, the program writes the chunks to create the whole video file.Load balancing functionality is achieved by creating a list of total segments and received segments at the client side.Resume functionality is achieved by saving all the data,segment number,downloaded bytes,total bytes,downloaded speed into a file.


Implementation Details:

Libraries used:

We have used mainly three libraries for making this project. These are given as:
1.Socket:
Socket library was used to create sockets for both the servers and client. Using the socket library is important for establishing a connection between client and server for communication. File is transferred over this link.
2.Threading:
Threads are used in this project because we needed to run several tasks at the same time in this project. 
3.Time:
The time library is important for measuring response time, waiting time, and measuring the efficiency of code.


Procedures and Functions :
All of the required functionality has been implemented at the server and client side through a modular approach by defining functions and invoking them at the required time. 
Functions at the server side : server start,sending file,sending file size,reporting,server close.Functions at the client side :  start (for taking inputs),connect with client,file receive,remaining segments(for load balancing),resume 