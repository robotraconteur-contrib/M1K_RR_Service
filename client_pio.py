#Simple example Robot Raconteur client light up M1K led
from RobotRaconteur.Client import *
import time
####################Start Service and robot setup
url='rr+tcp://localhost:11111?service=m1k'
m1k_obj = RRN.ConnectService(url)

#toggle PIO on/off
while True:
	m1k_obj.setpio('PIO_3',1)
	print(m1k_obj.getpio('PIO_3'))
	time.sleep(1)
	m1k_obj.setpio('PIO_3',0)
	print(m1k_obj.getpio('PIO_3'))
	time.sleep(1)
	