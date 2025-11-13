from mininet.net import Mininet
from mininet.topo import Topo
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import setLogLevel
from mininet.node import OVSKernelSwitch, RemoteController

class NetworkTopo(Topo):

	def build(self, **_opts):
                
        spines = {
            's5': self.addSwitch('spine5'),
            's6': self.addSwitch('spine6')
        }
        
        leaves = {
            'l1': self.addSwitch('leaf1'),
            'l2': self.addSwitch('leaf2'),
            'l3': self.addSwitch('leaf3'),
            'l4': self.addSwitch('leaf4')
        }
        
        hosts = {
            'h1': self.addHost('pc1'),
            'h2': self.addHost('pc2'),
            'h3': self.addHost('pc3'),
            'h4': self.addHost('pc4'),
            'h5': self.addHost('pc5'),
            'h6': self.addHost('pc6')
        }
		
		# spine-leaf connections (full-mesh)
		
		for s in spines:
			for l in leaves:
				self.addLink(spines[s], leaves[l])
				
		# host-leaf connections 
		
        self.addLink(hosts['h1'], leaves['l1']) 
        self.addLink(hosts['h2'], leaves['l1'])
        
        self.addLink(hosts['h3'], leaves['l2']) 
        
        self.addLink(hosts['h4'], leaves['l3']) 
        self.addLink(hosts['h5'], leaves['l3'])
        
        self.addLink(hosts['h6'], leaves['l4']) 
		
		
topos = {'SpineLeafTopo' : (lambda : NetworkTopo())}
		
		
		
