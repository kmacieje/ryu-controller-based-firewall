from mininet.net import Mininet
from mininet.topo import Topo
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import setLogLevel
from mininet.node import OVSKernelSwitch, RemoteController
import time
import random
import os

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
            'h1': self.addHost('pc1', ip='192.168.10.1/24'),
            'h2': self.addHost('pc2', ip='192.168.10.2/24'),
            'h3': self.addHost('pc3', ip='192.168.10.3/24'),
            'h4': self.addHost('pc4', ip='192.168.10.4/24'),
            'h5': self.addHost('pc5', ip='192.168.10.5/24'),
            'h6': self.addHost('pc6', ip='192.168.10.6/24')
        }
		
		# spine-leaf connections (full-mesh)
		
		for s in spines:
			for l in leaves:
				self.addLink(spines[s], leaves[l], cls=TCLink, bw=10)
				
		# host-leaf connections 
		self.addLink(hosts['h1'], leaves['l1']) 
		self.addLink(hosts['h2'], leaves['l1'])

		self.addLink(hosts['h3'], leaves['l2']) 

		self.addLink(hosts['h4'], leaves['l3']) 
		self.addLink(hosts['h5'], leaves['l3'])

		self.addLink(hosts['h6'], leaves['l4']) 

#topos = {'SpineLeafTopo' : (lambda : NetworkTopo())}

def run():
    topo = NetworkTopo()
    
    net = Mininet(
        topo = topo,
        controller = lambda name: RemoteController(
            name,
            ip = '127.0.0.1',
            port = 6633
        ),
        switch = OVSKernelSwitch,
        link = TCLink,
        autoSetMacs = True,
        autoStaticArp = True
    )

    net.start()
    pc1, pc2, pc3, pc4, pc5, pc6 = net.get('pc1', 'pc2', 'pc3', 'pc4', 'pc5', 'pc6')
    print('*** The network is running.')

    for s in net.switches:
        print(f'Setting configuration for {s}')
        os.system(f'ovs-vsctl set bridge {s} protocols=OpenFlow13')
        os.system(f'ovs-vsctl set-controller {s} tcp:127.0.0.1:6633')

    print('*** The network is setting STP')
    time.sleep(30)
	
    print('*** The network is ready for tests')
    print('*** Testing connectivity')
    net.pingAll()
	
    # servers, & makes it run in background
    pc3.cmd('iperf -s &')
    time.sleep(1)
	
    print('*** Normal traffic')
	# clients, popen runs the commends pararelly
    p1 = pc1.popen(f'iperf -c {pc3.IP()} -t 120 -i 5 > pc1_log_normal.txt', shell=True)
    time.sleep(random.uniform(0, 15))
    p2 = pc2.popen(f'iperf -c {pc3.IP()} -t 90 -i 5  > pc2_log_normal.txt', shell=True)
    time.sleep(random.uniform(0, 5))
    p4 = pc4.popen(f'iperf -c {pc3.IP()} -t 110 -i 5  > pc4_log_normal.txt', shell=True)
    time.sleep(random.uniform(0,20))
    p5 = pc5.popen(f'iperf -c {pc3.IP()} -t 60 -i 5  > pc5_log_normal.txt', shell=True)
	# waiting for the pararell processes so they can start togetheer
    p1.wait()
    p2.wait()
    p4.wait()
    p5.wait()
	
    print('*** Attack incoming')
    p1 = pc1.popen(f'iperf -c {pc3.IP()} -t 120 -i 5 > pc1_log_attack.txt', shell=True)
    time.sleep(random.uniform(0, 15))
	# SYN flood attack
    p6 = pc6.popen(f'hping3 -S --flood -p 5001 {pc3.IP()}', shell=True) 
    #p6 = pc6.popen(f'hping3 -S --flood -p 5001 {pc3.IP()}', shell=True) # we wanna use the same port as iperf
    time.sleep(60)
    p6.terminate()
    p6.wait()
    p1.wait()
    
    print('The attack is over!')

    CLI(net)
    net.stop()
            
# running the code
if __name__ == '__main__': 
	setLogLevel('info') 
	run()
		
