#!/usr/bin/env python
#import robotraconteur library
import RobotRaconteur as RR
RRN=RR.RobotRaconteurNode.s

import sys, time, threading, copy
import numpy as np
from pysmu import Session, LED, Mode

class m1k(object):
    #initialization
    def __init__(self):
        #start session
        self.session = Session()
        #get device
        self.device=self.session.devices[0]
        #streaming parameters
        self._streaming=False
        self._lock=threading.RLock()
        #mode 
        self.mode_dict={'HI_Z': Mode.HI_Z,'SVMI': Mode.SVMI,'SIMV':Mode.SIMV}
        self.sample=RRN.NewStructure("edu.rpi.robotics.m1k.sample")


    def setmode (self, channel, mode):
        self.device.channels[channel].mode =self.mode_dict[mode]
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
                reading=self.device.get_samples(1)[0]
                self.sample.A=reading[0]
                self.sample.B=reading[1]
                self.samples.OutValue=self.sample

    def getsample(self,number):
        sample_list=[]        

        for sample in self.session.get_samples(1000)[0]:
            self.sample.A=sample[0]
            self.sample.B=sample[1]
            sample_list.append(copy.deepcopy(self.sample))
        return sample_list



with RR.ServerNodeSetup("M1K_Service_Node", 11111):
    #Register the service type
    RRN.RegisterServiceTypeFromFile("edu.rpi.robotics.m1k")

    m1k_obj=m1k()

    #Register the service with object m1k_obj
    RRN.RegisterService("m1k","edu.rpi.robotics.m1k.m1k_obj",m1k_obj)

    #Wait for program exit to quit
    input("Press enter to quit")
    #shutdown
    sys.exit(1)