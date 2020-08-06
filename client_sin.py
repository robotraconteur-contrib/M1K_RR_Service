#Simple example Robot Raconteur client write sin wave to channel A, connect to B and read B
#Available waveforms: sine, triangle, sawtooth, square, stairstep

from RobotRaconteur.Client import *
#waveform plotting
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation

#plot settings
fig = plt.figure()
ax = plt.axes(xlim=(0, 2), ylim=(0, 5))
line, = ax.plot([], [], lw=2)
periodvalue=100
x = np.linspace(0, 2, periodvalue)
y = np.zeros(periodvalue)
samples_wire=None
def init():
	line.set_data([], [])
	return line,

def animate(i):
	global samples_wire,x,y
	y=np.roll(y,1)
	y[0]=samples_wire.InValue.B[0]

	# y = np.sin(2 * np.pi * (x - 0.01 * i))
	line.set_data(x, np.array(y))
	return line,


####################Start Service and robot setup
url='rr+tcp://localhost:11111?service=m1k'
m1k_obj = RRN.ConnectService(url)

#set mode for each channel
m1k_obj.setmode('A','SVMI')
m1k_obj.setmode('B','HI_Z')
#output waveform 

m1k_obj.wave('A', 'sine', 0, 5, periodvalue, -(periodvalue / 4), 0.5)

#start streaming samples
try:
	samples=m1k_obj.StartStreaming()
except:
	pass
#connect to wire
samples_wire=m1k_obj.samples.Connect()

#plot waveform
anim = animation.FuncAnimation(fig, animate, init_func=init,
							   frames=200, interval=20, blit=True)
plt.title("write A, read B")
plt.show()

#stop streaming
m1k_obj.StopStreaming()

