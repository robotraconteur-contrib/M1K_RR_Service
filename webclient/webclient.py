from js import print_div
from js import document
from js import ImageData
from RobotRaconteur.Client import *
from matplotlib import pyplot as plt
import numpy as np
import time
import warnings


periodvalue=100
x = np.linspace(0, 2, periodvalue)
y = np.zeros(periodvalue)

async def client_matplotlib():

	try:
		#connect to service
		url='rr+ws://localhost:11111/?service=m1k'
		m1k_obj=await RRN.AsyncConnectService(url,None,None,None,None)
		m1k_obj.async_StartStreaming(None)

		sub=RRN.SubscribeService(url)
		# while True:
			# try:
		set ROBOTRACONTEUR_LOG_LEVEL="DEBUG"
		m1k_obj = sub.GetDefaultClient()
		samples_wire=sub.SubscribeWire("samples_wire")
				# break
			# except RR.ConnectionException:
			# 	print_div("here")
			# 	time.sleep(0.1)

		print_div("Running!")
		#set mode for each channel
		m1k_obj.async_setmode('A','SVMI',None)
		m1k_obj.async_setmode('B','HI_Z',None)
		#start waveform
		m1k_obj.async_wave('A', 'triangle', 0, 5, periodvalue, -(periodvalue / 4), 0.5, None)
		

		fig, ax = plt.subplots()
		fig.show()	

		while True:
			await animate(0,m1k_obj,samples_wire,ax)

			await RRN.AsyncSleep(0.01,None)

	except:
		import traceback
		print_div(traceback.format_exc())
		m1k_obj.async_StopStreaming(None)
		raise

async def animate(i, m1k_obj,samples_wire,ax):
	global x, y
	try:
		# sample=samples_wire.InValue()
		sample=await m1k_obj.samples.AsyncPeekInValue(None)
		y=np.roll(y,1)
		y[0]=sample[0].B[0]
		# Draw x and y lists
		ax.clear()
		ax.plot(x, y,'ro')

		#text display
		props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
		text_m1k = '\n'.join((
		r'$ChA:V=%.2f$' % (sample[0].A[0], ),
		r'$ChA:I=%.2f$' % (sample[0].A[1], ),
		r'$ChB:V=%.2f$' % (sample[0].B[0], ),
		r'$ChB:I=%.2f$' % (sample[0].B[1], )))

		ax.text(0.75, 0.95, text_m1k, transform=ax.transAxes, fontsize=14,
				verticalalignment='top', bbox=props)
	except:
		pass


RR.WebLoop.run(client_matplotlib())