#Simple example Robot Raconteur client read number of samples
from RobotRaconteur.Client import *
from matplotlib import pyplot as plt
####################Start Service and robot setup
url='rr+tcp://localhost:11111?service=m1k'
m1k_obj = RRN.ConnectService(url)

#set mode for each channel
m1k_obj.setmode('A','SVMI')
m1k_obj.setmode('B','HI_Z')
m1k_obj.wave('A', 'sine', 0, 5, 100, -(100 / 4), 0.5)

#read 2000 samples
samples=m1k_obj.read(2000)



y=[]
for sample in samples:
	print("{: 6f} {: 6f} {: 6f} {: 6f}".format(sample.A[0], sample.A[1], sample.B[0], sample.B[1]))
	y.append(sample.A[0])
plt.plot(y)
plt.show()
