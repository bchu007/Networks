import socket
import sys
from thread import *
import re


# Steps from Root Bridge
RootCost = 0

# concat of priority and MAC address 
MyBID

# BID of root
RootBID


# get IP and Mac


# each host has unique IP, MAC, and has 3 ports


Ports = {}

# look at root cost
# look at lowest BID
# look at lowest neighbor port priority
# look at lowest neighbor port number

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    try:
	s.connect(('10.255.255.255', 1))
	IP = s.getsockname()[0]
    except:
	IP = '127.0.0.1'
    finally:
	s.close()
    return IP


#Function for handling connections. This will be used to create threads
def clientthread(conn):
    myList.append(conn) 
    #Sending message to connected client
    conn.send('Welcome to node ' + NODE + '. Type something and hit enter\n') #send only takes string
     
    #infinite loop so that function do not terminate and thread do not end.
    while True:
         
        #Receiving from client
        data = conn.recv(1024)
        reply = 'OK...' + data
    
    datalist = data.split()

    if len(datalist) < 1: 
        break
    # end 
        elif datalist[0] == '!q':
        print 'exiting...'
            break
    # pingmac <ip addr / mac addr>
    elif datalist[0] == 'pingmac' and datalist[1]: 
        p = getPort(datalist[1])
        
        # fails to return a valid port address
        if p < -1:
	continue
        
        # send a ping to port 
        x = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        x.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
        host = socket.gethostbyname('localhost') 
        x.connect((host, int(p)))
        x.send('pinging ' + datalist[1])
        x.recv(1024)

        # print arp response
        print x.recv(1024)
        x.close()
    # receiving ARP request
    elif datalist[0] == '1':
        # check if matches own MAC or IP 
        if datalist[3] == MAC or datalist[4] == IP:
	# add to our arp list
	iplist[datalist[2]] = datalist[1]
	maclist[datalist[1]] = datalist[5]

	# generate and return arp reply
	arpReply = '2 ' + datalist[1] + ' ' + datalist[2] + ' ' + str(MAC) + ' ' + str(IP) + ' '  + str(PORT)
	conn.send(arpReply)
    
    # receive ping request
    elif datalist[0] == 'pinging':

        # check if right ip/mac address   
        if (ipAddr.match(IP) or datalist[1] is IP) or (macAddr.match(IP) or datalist[1] is MAC):
	conn.send('pingmac received')
        else:
	continue
    
    # receive pingback 
    elif datalist[0] == 'pingback':
        if datalist[1] in (iplist.values() or ip.keys()):
	print 'pingmac received' 
	 
    elif datalist[0] == 'arp-a':
        print 'arp-a' 
        for i in iplist:
	print '? (' + i + ") at " + iplist[i] + " on port " + maclist[iplist[i]] 
        else: 
            conn.sendall(reply)
     
    #came out of loop
    conn.close()
 
#now keep talking with the client
while 1:
    #wait to accept a connection - blocking call
    conn, addr = s.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])
     
    #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
    start_new_thread(clientthread ,(conn,))
 
s.close()
