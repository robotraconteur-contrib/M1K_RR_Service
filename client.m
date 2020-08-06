m1k_obj=RobotRaconteur.ConnectService('rr+tcp://localhost:11111?service=m1k');

%set mode for each channel
m1k_obj.setmode('A','SVMI');
m1k_obj.setmode('B','HI_Z');
m1k_obj.wave('A', 'sine', 0, 5, 100, -(100 / 4), 0.5);

%read 2000 samples
samples=m1k_obj.read(int16(2000));



y=zeros(length(samples));
for i=1:length(samples)
	y(i)=samples{i}.A(1);
end

plot(y)
