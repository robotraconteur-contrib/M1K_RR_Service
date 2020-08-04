#Simple example Robot Raconteur client light up M1K led
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
		obj = sub.GetDefaultClient()
		samples_wire=sub.SubscribeWire("samples")
		break
	except RR.ConnectionException:
		time.sleep(0.1)

m1k_obj.setmode('A','HI_Z')
m1k_obj.setmode('B','HI_Z')
samples=m1k_obj.StartStreaming()
while True:
	if samples_wire.TryGetInValue()[0]:
		sample=samples_wire.InValue
	output("{: 6f} {: 6f} {: 6f} {: 6f}".format(sample.A[0], sample.A[1], sample.B[0], sample.B[1]))