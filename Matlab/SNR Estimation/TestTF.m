clc;
close all;
frequency=25;
duration=30;
amplitude=10;
Fs=500;
zetaError=0.0000001;
w0Error=0.000001;

% Sinal de EEG limpo
[basisSignal,t]=generate_sine_wave(25,duration,10,Fs);
cleanEEG=awgn(basisSignal,5,'measured');

% Sinal de referência para estimativa de SNR
[basisSignal2,t]=generate_sine_wave(5,duration,8,Fs);
cleanEEG2=awgn(basisSignal2,6,'measured');

% Sinal de estimulação
[pureStimulation,t]=generate_sine_wave(21,duration,800,Fs);
L=size(t,2);
stimulation=awgn(pureStimulation,90,'measured');

% Função de transferência 'real'
w0=1;
zeta=0.0005;
numerator=w0^2;
denominator=[1,2*zeta*w0,w0^2];
bodyTf=tf(numerator,denominator,1/Fs);

% Geração do sinal de artefato
stimulationSignal=lsim(bodyTf,stimulation,t)';
actualNoise=awgn(stimulationSignal,50,'measured');

% Função de transferência estimada
estimatedw0=w0+w0Error;
estimatedzeta=zeta+zetaError;
estimatednumerator=estimatedw0^2;
estimateddenominator=[1,2*estimatedzeta*estimatedw0,estimatedw0^2];
estimatedTf=tf(estimatednumerator,estimateddenominator,1/Fs);

% Estimativa do sinal de artefato
expectedNoise=lsim(estimatedTf,pureStimulation)';

% Sinal poluído
dirtySignal=cleanEEG+actualNoise;
% FFTs
dirtyFFT=fft(dirtySignal);
noiseFFT=fft(expectedNoise);

% Reconstrução
cleanReconstruction=ifft(dirtyFFT-noiseFFT);

% Estimativa de SNRs
pre=snr_clean_reference(cleanEEG2,dirtySignal);
post=snr_clean_reference(cleanEEG2,cleanReconstruction);
disp(strcat('SNR Estimado Referencia/Limpo: ',sprintf('%.4f',snr_clean_reference(cleanEEG2,cleanEEG)),'dB'));
disp(strcat('SNR Estimado PRE: ',sprintf('%.4f',pre),'dB'));
disp(strcat('SNR Estimado POST: ',sprintf('%.4f',post),'dB'));
disp(strcat('Taxa de redução de artefato: ',sprintf('%.4f',pre/post)));

% Plots
figure(1),subplot(3,1,1),plot(dirtySignal),title('Sinal corrompido');
figure(1),subplot(3,1,2), plot(cleanReconstruction);
hold on;
plot(cleanEEG);
hold off;
legend('recovered','original'),title('Reconstrução vs Sinal Limpo Original');

figure(1),subplot(3,1,3), plot(cleanReconstruction-cleanEEG),title('Erro de reconstrução');