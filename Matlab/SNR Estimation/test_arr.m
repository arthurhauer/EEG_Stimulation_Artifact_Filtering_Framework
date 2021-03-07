Fs=500;
duration=10;
frequency1=20;
frequency2=25;
amplitude=0.05;

cleanSignal1=generate_sine_wave(frequency1,duration,amplitude,Fs);
cleanSignal2=generate_sine_wave(frequency2,duration,amplitude,Fs);
[estimatedCleanSNR,f]=snr_estimation(cleanSignal1,cleanSignal2,Fs);
figure(1),subplot(2,1,1),plot(f,estimatedCleanSNR);

signal1=generate_repeatable_awgn(cleanSignal1,10);
signal2=generate_repeatable_awgn(cleanSignal2,10);
[estimatedSNR,f]=snr_estimation(signal1,signal2,Fs);
figure(1),subplot(2,1,2),plot(f,estimatedSNR);
