# commands 
'''python arp.py <NODE>/<ip address><mac address><port>'''
runs the script where <NODE> can be either 'A', 'B', 'C', or 'D' which has preset <ip addresses>, <mac addresses>, and <ports>. These presets can be manually inputted as well.

## presets node parameters
<table>
  <tr>
    <th>node</th>
    <th>ip addresses</th>
    <th>mac addresses</th>
    <th>ports</th>
  </tr>
  <tr>
    <th>A</th>
    <th>10.0.100.2</th>
    <th>08:00:27:26:03:93</th>
    <th>8000</th>
  </tr>
    <th>B</th>
    <th>10.0.100.3</th>
    <th>08:00:27:58:32:0d</th>
    <th>8001</th>
  <tr>
    <th>C</th>
    <th>10.0.100.4</th>
    <th>08:00:27:58:68:98</th>
    <th>8002</th>
  </tr>
  <tr>
    <th>D</th>
    <th>10.0.100.4</th>
    <th>00:24:1d:5c;5b:dc</th>
    <th>8003</th>
  </tr>
</table>

'''pingmac <ipaddress/macaddress>'''
pings node. checks if address is inside current arp table, otherwise broadcast to all other port arp entry. request arp response entry and fill in arp table. Ping respective node and receive confirmation.

'''arp-a'''
prints out a list of <ip addresses> <mac addresses> and <ports> inside of arp table of current node.


 
