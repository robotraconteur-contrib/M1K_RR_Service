#Simple example Robot Raconteur client read number of samples
from RobotRaconteur.Client import *
from matplotlib import pyplot as plt
import time
####################Start Service and robot setup
url='rr+tcp://localhost:11111?service=m1k'
m1k_obj = RRN.ConnectService(url)

#set mode for each channel
m1k_obj.setmode('A','SVMI')
m1k_obj.setmode('B','HI_Z')
m1k_obj.wave('A', 'sine', 0, 5, 100, -(100 / 4), 0.5)

#read 2000 samples
samples=m1k_obj.read(2000)

print(time.time()-samples.timestamp)

# y=[]
# for i in range(int(len(samples.data)/4)):
# 	print("{: 6f} {: 6f} {: 6f} {: 6f}".format(samples.data[4*i], samples.data[4*i+1], samples.data[4*i+2], samples.data[4*i+3]))
# 	y.append(samples.data[4*i])
# plt.plot(y)
# plt.show()
