# Robot Raconteur M1K Board Service
## Prerequisites
* [RobotRaconteur](https://github.com/robotraconteur/robotraconteur/wiki/Download)
* [Python bindings](https://github.com/analogdevicesinc/libsmu) (python3.7)

For Windows, the python bindings could be installed together with [PixelPulse2](https://wiki.analog.com/university/tools/m1k/pixelpulse) Software

## Service Definition
```
service edu.rpi.robotics.m1k

stdver 0.9
struct sample
	field double[] A
	field double[] B
end

object m1k_obj
	function void setmode (string channel, string mode)
	function void setled(int8 val)
	function sample{list} read(int16 number)
	function void write(string channel, double val)
	function void setpio(string port, int8 val)
	function double getpio(string port)
	wire sample samples [readonly]
	function void StartStreaming()
	function void StopStreaming()
	function void wave(string channel, string wavename, double value1, double value2, double periodvalue, double delayvalue, double dutycyclevalue)
end
```
## Usage:
Simply run `$ python m1k_service.py` to start the RR service.

## Example Clients:
`client_led.py`:        light up on-board LED in binary format

`client_read.py`:       get a number of samples from the board 

`client_streaming.py`:  get real time reading from the board

`client_write.py`:      write the output to the board channel

`client_pio.py`:	toggle the pio pins on/off

`client_sin.py`:	generate sine wave to channel A, connect channel A to B IN, display reading from channel B
