function [signal,t] = generate_sine_wave(frequency,duration,amplitude,Fs)
ts=1/Fs;
t=0:ts:duration;
signal=sin(2*pi*frequency*t)*amplitude;
end

