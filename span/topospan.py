#!/usr/bin/python

from mininet.node import Host, OVSSwitch, Controller
from mininet.link import Link

h1 = Host( 'b1' );
h2 = Host( 'b2' );
h3 = Host( 'b3' );
h4 = Host( 'b4' );
s1 = OVSSwitch( 's1', inNamespace=False )
c0 = Controller( 'c0', inNamespace=False )
Link( h1, s1 )
Link( h2, s1 )
Link( h3, s1 )
Link( h4, s1 )
h1.setIP( '10.0.0.1/24' )
h2.setIP( '10.0.0.2/24' )
h3.setIP( '10.0.0.3/24' )
h4.setIP( '10.0.0.4/24' )
c0.start()
s1.start( [ c0 ] )
print h1.IP
print h2.IP
print h3.IP
print h4.IP
s1.stop()
c0.stop()

