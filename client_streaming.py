#Simple example Robot Raconteur client get real time reading from both channels
from RobotRaconteur.Client import *
import sys, time

if sys.stdout.isatty():
    output = lambda s: sys.stdout.write("\r" + s)
else:
    output = print

####################Start Service and robot setup
url='rr+tcp://localhost:11111?service=m1k'
sub=RRN.SubscribeService(url)
while True:
	try:

		m1k_obj = sub.GetDefaultClient()
		break
	except RR.ConnectionException:
		time.sleep(0.1)
#subscribe to wire
samples_wire=sub.SubscribeWire("samples")
# m1k_obj.setmode('A','HI_Z')
# m1k_obj.setmode('B','HI_Z')
m1k_obj.sample_size=100
try:
	samples=m1k_obj.StartStreaming()
except:
	pass

timestamp=None
while True:
	sample_packet=samples_wire.TryGetInValue()
	if (not sample_packet[0]) or sample_packet[-1]==timestamp:
		continue
	samples=sample_packet[1]
	timestamp=sample_packet[-1]	
	for i in range(int(len(samples)/4)):
		output("{: 6f} {: 6f} {: 6f} {: 6f}".format(samples[4*i], samples[4*i+1], samples[4*i+2], samples[4*i+3]))

#stop streaming
m1k_obj.StopStreaming()