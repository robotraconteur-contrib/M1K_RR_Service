#Simple example Robot Raconteur client write to both channels
from RobotRaconteur.Client import *
import numpy as np
import time
####################Start Service and robot setup
url='rr+tcp://localhost:11111?service=m1k'
m1k_obj = RRN.ConnectService(url)

#set mode for each channel
m1k_obj.setmode('A','SVMI')
time.sleep(1)
m1k_obj.setmode('B','SVMI')
time.sleep(1)
#write
m1k_obj.write('A',5.*np.random.random(100))
m1k_obj.write('B',[1.])