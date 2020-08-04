#Simple example Robot Raconteur client light up M1K led
from RobotRaconteur.Client import *

####################Start Service and robot setup
url='rr+tcp://localhost:11111?service=m1k'
m1k_obj = RRN.ConnectService(url)

m1k_obj.setmode('A','HI_Z')
m1k_obj.setmode('B','HI_Z')
samples=m1k_obj.getsample(1000)
for sample in samples:
	print("{: 6f} {: 6f} {: 6f} {: 6f}".format(sample.A[0], sample.A[1], sample.B[0], sample.B[1]))