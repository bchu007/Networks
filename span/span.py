import socket
import sys
from thread import *
import threading
import re
import commands
from uuid import getnode as get_mac




# Steps from Root Bridge
RootCost = 0
StatusTable = []
PortMap = []
MyPortMap = {}
MyBID
RootBID
Cost



def get_ips(): 
    ips = commands.getoutput("/sbin/ifconfig | grep -i \"inet\" | awk '{print $5}'")
    return ips

def get_macs():
    macs = commands.getoutput("/sbin/ifconfig | grep -i \"HWaddr\" | awk '{print $5}'")
    return macs


if len(sys.argv) == 0:
    MyBID =  '32768' + get_macs()
    RootBID = MyBID
elif len(sys.argv) == 1:
    MyBID = sys.argv + get_macs()
    RootID = MyBID

    


# each host has unique IP, MAC, and has 3 ports
for i in range(1,3):
    StatusTable.append(["",i,""])

#hard coded forwarding ports
NodeIP = {1 : "10.0.0.1", 2 : "10.0.0.2", 3 : "10.0.0.3", 4 : "10.0.0.4"}
IPNode = {"10.0.0.1" : 1, "10.0.0.2" : 2, "10.0.0.3" : 3, "10.0.0.4" : 4}
PortMap.append( [ 1, 2, 3] )
PortMap.append( [ 1, 3, 1] )
PortMap.append( [ 1, 4, 2] )
PortMap.append( [ 2, 1, 3] )
PortMap.append( [ 2, 3, 2] )
PortMap.append( [ 2, 4, 1] )
PortMap.append(	[ 3, 1, 1] ) 
PortMap.append( [ 3, 2, 2] ) 
PortMap.append( [ 3, 4, 3] ) 
PortMap.append( [ 4, 1, 2] )
PortMap.append( [ 4, 2, 1] )
PortMap.append( [ 4, 3, 3] )


def set_timer(duration):
    threading.Timer(durration, set_timer).start()


# creates a port map for this node as a dictionary that maps dest to port
def gen_outNode(IP):
    for entry in PortMap:
	if entry[0] == IPNode[IP]:
	    MyPortMap[entry[1]] = entry[2]
	    
	    
		    
        	    	


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



def elect_root(bpdu): 
    #compare with own bpdu
	
	


#Function for handling connections. This will be used to create threads
def clientthread(conn):
    myList.append(conn) 
    #Sending message to connected client
    conn.send('Welcome to node ' + NODE + '. Type something and hit enter\n') #send only takes string
     
    #infinite loop so that function do not terminate and thread do not end.
    while True:
        

	if MyBID == RootBID:

	    #send to all other ports
	    get_outNode(IPNode[get_ip()])
	    for portconn in MyPortMap:
		out_ip = NodeIP[portconn[0]]
		out_port = portconn[1]
	    
	    x = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	    x.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
	    host = socket.gethostbyname() 


	    
        #Receiving from client
        data = conn.recv(1024)
        reply = 'OK...' + data
    
	datalist = data.split()

	elif datalist[0] == '!q':
	    print 'exiting...'
            break
	# pingmac <ip addr / mac addr>
	elif datalist[0] == 'BPDU': 
	    elect_root(datalist[1:])
        
	elif datalist[0] == 't':
	    
        # fails to return a valid port address
        if p < -1:
	    continue
        
	    # send a ping to port 
	   
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
