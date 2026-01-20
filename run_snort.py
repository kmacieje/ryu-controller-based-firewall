import os
import sys
import time
    
    
target_interfaces = ['leaf1-eth3', 'leaf1-eth4', 'leaf2-eth3', 'leaf3-eth3', 'leaf3-eth4', 'leaf4-eth3']
print('*** Starting Snort on specific interfaces...')
    
for intf in target_interfaces:
	os.system(f"sudo snort -i {intf} -A unsock -l /tmp -c /etc/snort/snort.conf > /dev/null 2>&1 &")
