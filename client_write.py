#Simple example Robot Raconteur client write to both channels
from RobotRaconteur.Client import *

####################Start Service and robot setup
url='rr+tcp://localhost:11111?service=m1k'
m1k_obj = RRN.ConnectService(url)

#set mode for each channel
m1k_obj.setmode('A','SVMI')
m1k_obj.setmode('B','SVMI')
#write
m1k_obj.write('A',2.5)
m1k_obj.write('B',1)