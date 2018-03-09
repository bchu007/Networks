import socket
import sys
from thread import *
import re


HOST = ''   # Symbolic name meaning all available interfaces
PORT = 8000 # Arbitrary non-privileged port
myList = []
datalist = []
maclist = {}
iplist = {}
portlist = [8000, 8001, 8002, 8003]

if len(sys.argv) == 2:
	#choses what node to use
	NODE = sys.argv[1] 
	print NODE

	if NODE == 'A':
		IP = '10.0.100.2'
		MAC = '08:00:27:26:03:93'
		PORT = 8000
	elif NODE == 'B':
		IP = '10.0.100.3'
		MAC = '08:00:27:58:32:0d'
		PORT = 8001
	elif NODE == 'C':
		IP = '10.0.100.4'
		MAC = '08:00:27:58:68:98'
		PORT = 8002
	elif NODE == 'D':
		IP = '10.0.100.5'
		MAC = '00:24:1d:5c:5b:dc'
		PORT = 8003
elif len(sys.argv) == 4:
	IP = sys.argv[1]
	MAC = sys.argv[2]
	PORT = sys.argv[3]
else:
	print "wrong number of parameters: " + len(sys.argv)

#server socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)

#client socket
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)

except socket.error:
    print 'Failed to create socket'
    sys.exit()
     

print 'Socket created'
 
#Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error , msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
     
print 'Socket bind complete'
 
#Start listening on socket
s.listen(10)
print 'Socket now listening'

macAddr = re.compile('([0-9a-fA-F]{2}[:-]){5}([0-9a-fA-F]{2})') 
ipAddr = re.compile('((2[0-5]|1[0-9]|[0-9])?[0-9]\.){3}((2[0-5]|1[0-9]|[0-9])?[0-9])') 
#Function that gets port number given ip or mac addr
def getPort(addr):
    
    if macAddr.match(addr):
	#check if address is in the list
	if addr in maclist:
	    return addr
	else:
	    #remove current port
	    if PORT in portlist:
		portlist.remove(PORT)
	    #iterate and send message to the rest.
	    for port in portlist:
		try:
		    x = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		    x.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
		
		    arpEntry = '1 ' + str(MAC) + ' ' + str(IP) + ' ' + str(addr) + ' '  + '0.0.0.0 ' + str(PORT)	
		    host = socket.gethostbyname('localhost') 
		    x.connect((host, port))
		    x.settimeout(0.01)
		    x.send(arpEntry)
		    x.recv(1024)
		    arpRet = x.recv(1024)
		    arpRetList = arpRet.split()
		    x.close()
		
		    if arpRetList[0] == '2' and macAddr.match(arpRetList[3]):
			# add to our arp list
			iplist[arpRetList[4]] = arpRetList[3]
			maclist[arpRetList[3]] = arpRetList[5]

			return arpRet[3]
		
		except socket.timeout:
		    pass
    
	    print 'returned arp fails: MAC address'
	    return -1
    elif ipAddr.match(addr):
	
	#check if address is in the list
	if addr in iplist:
	    return maclist[addr]
	else:
	    #remove current port
	    if PORT in portlist:
		portlist.remove(PORT)
	    #iterate and send message to the rest.
	    for port in portlist:
		try:
		    x = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		    x.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)

		    arpEntry = '1 ' + str(MAC) + ' ' + str(IP) + ' ' +  '00:00:00:00:00:00 ' + str(addr) + ' ' + str(PORT)	
		    
		    host = socket.gethostbyname('localhost') 
		    x.connect((host, port))
		    x.settimeout(0.01)
		    x.send(arpEntry)
		    x.recv(1024)
		    arpRet = x.recv(1024)
		    arpRetList = arpRet.split()
		    x.close()
		    
		    if arpRetList[0] == '2' and macAddr.match(arpRetList[3]):
			# add to our arp list
			iplist[arpRetList[4]] = arpRetList[3]
			maclist[arpRetList[3]] = arpRetList[5]
			
			return arpRetList[5]

		except socket.timeout:		         	
		    pass

	    print 'returned arp fails: IP address'
	    return -1


    else:
	print 'not a valid address: cannot find with broadcast'
 


 
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
