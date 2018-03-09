from mininet.top import Topo

class STPTopo( Topo ):
	def__init__( self ):
		# Initialize topology
		Topo.__init__( self )
		# Add hosts and switches
		h1 = self.addHost( 'b1' )
		h2 = self.addHost( 'b2' )
		h3 = self.addHost( 'b3' )
		h4 = self.addHost( 'b4' )
		switch = self.addSwitch( 's1' )
		# Add Links
		self.addLink( h1, switch )
		self.addLink( h2, switch )
		self.addLink( h3, switch )
		self.addLink( h4, switch )

topos = { 'stptopo' : ( lambda: STPTopo() ) }

		

