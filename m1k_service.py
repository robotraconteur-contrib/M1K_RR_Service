#!/usr/bin/env python
#import robotraconteur library
import RobotRaconteur as RR
RRN=RR.RobotRaconteurNode.s

import sys, time, threading, copy, traceback
import numpy as np
from pysmu import Session, LED, Mode

class m1k(object):
    #initialization
    def __init__(self):
        #start session
        self.session = Session()
        #get device
        try:
            self.device=self.session.devices[0]
        except IndexError:
            print("No Device Found")
            sys.exit(1)

        #streaming parameters
        self._streaming=False
        self._lock=threading.RLock()
        #mode 
        self.mode_dict={'HI_Z': Mode.HI_Z,'SVMI': Mode.SVMI,'SIMV':Mode.SIMV}
        self.port_dict={'PIO_0': 28,'PIO_1': 29,'PIO_2': 47,'PIO_3': 3}
        self.sample=RRN.NewStructure("edu.rpi.robotics.m1k.sample")
        #wave dict
        self.wavedict = {
        ('A','sine'): self.device.channels['A'].sine,
        ('A','triangle'): self.device.channels['A'].triangle,
        ('A','sawtooth'): self.device.channels['A'].sawtooth,
        ('A','stairstep'): self.device.channels['A'].stairstep,
        ('A','square'): self.device.channels['A'].square,
        ('B','sine'): self.device.channels['B'].sine,
        ('B','triangle'): self.device.channels['B'].triangle,
        ('B','sawtooth'): self.device.channels['B'].sawtooth,
        ('B','stairstep'): self.device.channels['B'].stairstep,
        ('B','square'): self.device.channels['B'].square
        }


    def setmode (self, channel, mode):
        try:
            self.device.channels[channel].mode =self.mode_dict[mode]
        except:
            traceback.print_exc()
        return

    #set 3 leds on/off based on binary value (000~111)
    def setled(self,val):
        self.device.set_led(val)

    def StartStreaming(self):
        if (self._streaming):
            raise Exception("Already streaming")
        self._streaming=True
        t=threading.Thread(target=self.stream)
        t.start()

    #Stop the streaming thread
    def StopStreaming(self):
        if (not self._streaming):
            raise Exception("Not streaming")
        self._streaming=False

    def stream(self):
        while self._streaming:
            with self._lock:
                try:
                    reading=self.device.get_samples(1)[0]
                    self.sample.A=reading[0]
                    self.sample.B=reading[1]
                    self.samples.OutValue=self.sample
                except:
                    traceback.print_exc()

    def read(self,number):
        sample_list=[]        

        for sample in self.session.get_samples(1000)[0]:
            self.sample.A=sample[0]
            self.sample.B=sample[1]
            sample_list.append(copy.deepcopy(self.sample))
        return sample_list

    def write(self,channel, val):
        self.device.channels[channel].write([val]*self.session.queue_size)
        return

    def setpio(self,port,val):

        if val:
            self.device.ctrl_transfer(0x40, 0x51, self.port_dict[port], 0, 0, 0, 100) # set to 1
        else:
            self.device.ctrl_transfer(0x40, 0x50, self.port_dict[port], 0, 0, 0, 100) # set to 0
    #bug here
    def getpio(self,port):
        print(self.device.ctrl_transfer(0xc0, 0x91, self.port_dict[port], 0, 0, 1, 100))
        return self.device.ctrl_transfer(0xc0, 0x91, self.port_dict[port], 0, 0, 1, 100)

    

    def wave(self, channel, wavename, value1, value2, periodvalue, delayvalue, dutycyclevalue=0.5):
        if wavename=="square":
            self.wavedict[(channel,wavename)](value1, value2, periodvalue, delayvalue, dutycyclevalue)
        else:
            self.wavedict[(channel,wavename)](value1, value2, periodvalue, delayvalue)



with RR.ServerNodeSetup("M1K_Service_Node", 11111):
    #Register the service type
    RRN.RegisterServiceTypeFromFile("edu.rpi.robotics.m1k")

    m1k_obj=m1k()

    #Register the service with object m1k_obj
    RRN.RegisterService("m1k","edu.rpi.robotics.m1k.m1k_obj",m1k_obj)

    #Wait for program exit to quit
    input("Press enter to quit")
    sys.exit(1)
