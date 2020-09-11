ADISession = daq.createSession('adi')
% Add an analog output channel with device ID SMU1 and channel ID A,
% and set its measurement type to Voltage.
addAnalogOutputChannel(ADISession,'smu1','a','Voltage');
addAnalogInputChannel(ADISession,'smu1','a','Current');
addAnalogOutputChannel(ADISession,'smu1','b','Voltage');
addAnalogInputChannel(ADISession,'smu1','b','Current');



pdata = zeros(2100,1); % Column vector of 2100 samples.
pdata (1001:1100) = 5; % Pulse in middle of vector.

s = daq.createSession('adi');
addAnalogOutputChannel(s,'SMU1','B','Voltage');

queueOutputData(s,pdata);
s   % View channel configuration and scan settings.
