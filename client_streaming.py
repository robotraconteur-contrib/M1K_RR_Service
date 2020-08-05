#Simple example Robot Raconteur client get real time reading from both channels
from RobotRaconteur.Client import *
import sys, time

if sys.stdout.isatty():
    output = lambda s: sys.stdout.write("\r" + s)
else:
    output = print

####################Start Service and robot setup
url='rr+tcp://localhost:11111?service=m1k'
m1k_obj = RRN.ConnectService(url)
samples_wire=m1k_obj.samples.Connect()

# m1k_obj.setmode('A','HI_Z')
# m1k_obj.setmode('B','HI_Z')
try:
	samples=m1k_obj.StartStreaming()
except:
	pass
while True:
	if samples_wire.TryGetInValue()[0]:
		sample=samples_wire.InValue
		output("{: 6f} {: 6f} {: 6f} {: 6f}".format(sample.A[0], sample.A[1], sample.B[0], sample.B[1]))

#stop streaming
m1k_obj.StopStreaming()