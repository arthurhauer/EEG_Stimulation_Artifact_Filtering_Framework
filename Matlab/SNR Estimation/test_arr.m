Fs=500;
duration=10;
frequency=20;
amplitude=1;
stimulation_artifact_SNR=0.5;

basisSignal=generate_sine_wave(frequency,duration,amplitude,Fs); % Generate sinewave

cleanSignal1=awgn(basisSignal,10,'measured'); % Add white gaussian noise to act as commonly found noise in measurements
cleanSignal2=awgn(basisSignal,10,'measured'); %

[estimatedCleanSNR,f]=snr_estimation(cleanSignal1,cleanSignal2,Fs); % Estimate the 'clean signal' SNR
figure(1),subplot(3,1,1),plot(f,estimatedCleanSNR);

signal1=generate_repeatable_awgn(cleanSignal1,stimulation_artifact_SNR);% Add stimulation artifact noise
signal2=generate_repeatable_awgn(cleanSignal2,stimulation_artifact_SNR);

[estimatedSNR,f]=snr_estimation(signal1,signal2,Fs); % Estimate 'dirty' signal's SNR

figure(1),subplot(3,1,2),plot(f,estimatedSNR);