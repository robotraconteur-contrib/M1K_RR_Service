#Simple example Robot Raconteur client read number of samples
from RobotRaconteur.Client import *

####################Start Service and robot setup
url='rr+tcp://localhost:11111?service=m1k'
m1k_obj = RRN.ConnectService(url)

#set mode for each channel
m1k_obj.setmode('A','HI_Z')
m1k_obj.setmode('B','HI_Z')
#read 1000 samples
samples=m1k_obj.read(2000)
for sample in samples:
	print("{: 6f} {: 6f} {: 6f} {: 6f}".format(sample.A[0], sample.A[1], sample.B[0], sample.B[1]))

print(len(samples))