#Simple example Robot Raconteur client write sin wave to channel A, connect to B and read B
#Available waveforms: sine, triangle, sawtooth, square, stairstep

from RobotRaconteur.Client import *
#waveform plotting
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
import time

####################Start Service and robot setup
url='rr+tcp://localhost:11111?service=m1k'
########subscription mode
sub=RRN.SubscribeService(url)
while True:
	try:
		m1k_obj = sub.GetDefaultClient()
		samples_wire=sub.SubscribeWire("samples")
		break
	except RR.ConnectionException:
		time.sleep(0.1)

#streaming parameters
frequency=1000
periodvalue = int(m1k_obj.sample_rate/frequency)

#plot settings
time_axis=20	#ms, must be greater than 1/freq, default to be 1 period
cycles_onscreen=time_axis/(1000/frequency)

fig = plt.figure()
ax = plt.axes(xlim=(0, time_axis), ylim=(0, 5))
line, = ax.plot([], [], lw=2)

points_onscreen=int(time_axis*m1k_obj.sample_rate/1000)
m1k_obj.sample_size=int(points_onscreen/cycles_onscreen)

# m1k_obj.sample_size=10000

x = np.linspace(0, time_axis, points_onscreen)
y = np.zeros(points_onscreen)


timestamp=0
def init():
	line.set_data([], [])
	return line,

def animate(i):
	global samples_wire,x,y,timestamp
	sample_packet=samples_wire.TryGetInValue()
	if (not sample_packet[0]) or sample_packet[-1]==timestamp:
		return line,

	samples=sample_packet[1]
	timestamp=sample_packet[-1]	

	y=np.roll(y,m1k_obj.sample_size)


	y[:m1k_obj.sample_size]=samples[::4]

	line.set_data(x, np.array(y))

	return line,




#set mode for each channel
m1k_obj.setmode('A','SVMI')
# m1k_obj.setmode('B','HI_Z')
#output waveform 

# m1k_obj.wave('A', 'sine', 0, 5, periodvalue, -(periodvalue / 4), 0.5)
randomwaveform=5*np.random.random(100)
m1k_obj.arbitrary('A',randomwaveform)

#start streaming samples
try:
	samples=m1k_obj.StartStreaming()
except:
	pass

#plot waveform
anim = animation.FuncAnimation(fig, animate, init_func=init,
							   frames=200, interval=20, blit=True)
plt.title("write A, read A")
plt.show()

#stop streaming
m1k_obj.StopStreaming()

