#!/usr/bin/env python
#import robotraconteur library
import RobotRaconteur as RR
RRN=RR.RobotRaconteurNode.s

import sys, time, threading, copy, traceback
import numpy as np
from pysmu import Session, LED, Mode, exceptions

class m1k(object):
    #initialization
    def __init__(self):
        #start session
        self.session = Session()
        #define sample rate
        self.sample_rate=100000
        #define streaming sample size
        self.sample_size=1
        #get device
        try:
            self.device=self.session.devices[0]
        except IndexError:
            print("No Device Found")
            sys.exit(1)
        #initialize default mode to HI_Z
        self.device.channels['A'].mode=Mode.HI_Z
        self.device.channels['B'].mode=Mode.HI_Z
        #streaming parameters
        self._streaming=False
        self._lock=threading.RLock()
        #mode 
        self.mode_dict={'HI_Z': Mode.HI_Z,'SVMI': Mode.SVMI,'SIMV':Mode.SIMV}
        self.port_dict={'PIO_0': 28,'PIO_1': 29,'PIO_2': 47,'PIO_3': 3}
        # self.sample=RRN.NewStructure("edu.rpi.robotics.m1k.sample")
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
            self.StopStreaming()
            self.device.channels[channel].mode =self.mode_dict[mode]
            time.sleep(0.1)
            self.StartStreaming()
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
                    reading=self.device.get_samples(self.sample_size)
                    self.samples.OutValue=list(sum(sum(reading, ()),()))
                    # sample_list=[]  
                    # for i in range(self.sample_size):
                    #     self.sample.A=reading[0]
                    #     self.sample.B=reading[1]
                    #     sample_list.append(copy.deepcopy(self.sample))
                    # self.samples.OutValue=sample_list
                except exceptions.SessionError:
                    print("pysmu Session Error while streaming")
                    self._streaming=False
                    self.device.channels['A'].mode=Mode.HI_Z
                    self.device.channels['B'].mode=Mode.HI_Z
                    traceback.print_exc()
                    break
                except:
                    traceback.print_exc()

    def read(self,number):
        # sample_list=[]        
        # for sample in self.session.get_samples(number)[0]:
        #     self.sample.A=sample[0]
        #     self.sample.B=sample[1]
        #     sample_list.append(copy.deepcopy(self.sample))
        # return sample_list

        ########read number of samples, return 1D list [A_voltage,A_current,B_voltage,B_current,A_voltage,....]
        reading=self.device.get_samples(number)
        return list(sum(sum(reading, ()),()))

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



def main():
    with RR.ServerNodeSetup("M1K_Service_Node", 11111) as node_setup:
        #Register the service type
        RRN.RegisterServiceTypeFromFile("edu.rpi.robotics.m1k")

        m1k_obj=m1k()

        #Register the service with object m1k_obj
        RRN.RegisterService("m1k","edu.rpi.robotics.m1k.m1k_obj",m1k_obj)

        #add ws origin
        node_setup.tcp_transport.AddWebSocketAllowedOrigin("http://localhost")
        node_setup.tcp_transport.AddWebSocketAllowedOrigin("https://hehonglu123.github.io")

        #Wait for program exit to quit
        input("Press enter to quit")
        sys.exit(1)

        

if __name__ == '__main__':
    try:
        main()

    except exceptions.SessionError:
        print("Session Error, restarting service")
        main()
    except:
        traceback.print_exc()
    