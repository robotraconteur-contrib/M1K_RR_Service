#Simple example Robot Raconteur client light up M1K led
from RobotRaconteur.Client import *
from random import randrange
import time
####################Start Service and robot setup
url='rr+tcp://localhost:11111?service=m1k'
m1k_obj = RRN.ConnectService(url)

while True:
    val = randrange(0, 8)
    m1k_obj.setled(val)
    time.sleep(.25)