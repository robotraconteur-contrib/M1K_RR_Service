#Simple example Robot Raconteur client read number of samples
from RobotRaconteur.Client import *
from matplotlib import pyplot as plt
####################Start Service and robot setup
url='rr+tcp://localhost:11111?service=m1k'
m1k_obj = RRN.ConnectService(url)


mode=input("mode")
#set mode for each channel
m1k_obj.setmode('A',mode)
