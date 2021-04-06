function [qErrorSum,arr]=tf_estimation_cleanup(frequency,duration,amplitude,Fs,zetaError,w0Error,preStimulationSNR,postStimulationSNR,shouldPlot)
maxError=1e+200;
% Sinal de EEG limpo
[basisSignal,t]=generate_sine_wave(frequency(1),duration,amplitude(1),Fs);
cleanEEG=awgn(basisSignal,5,'measured');

% Sinal de referência para estimativa de SNR
[basisSignal2,t]=generate_sine_wave(frequency(2),duration,amplitude(2),Fs);
cleanEEG2=awgn(basisSignal2,6,'measured');

% Sinal de estimulação
[pureStimulation,t]=generate_sine_wave(frequency(3),duration,amplitude(3),Fs);
L=size(t,2);
stimulation=awgn(pureStimulation,preStimulationSNR,'measured');

% Função de transferência 'real'
w0=1;
zeta=0.0005;
bodyTf=tf(w0^2,[1,2*zeta*w0,w0^2],1/Fs);

% Geração do sinal de artefato
stimulationSignal=lsim(bodyTf,stimulation,t)';
actualNoise=awgn(stimulationSignal,postStimulationSNR,'measured');

% Função de transferência estimada
estimatedw0=w0+w0Error;
estimatedzeta=zeta+zetaError;
estimatedTf=tf(estimatedw0^2,[1,2*estimatedzeta*estimatedw0,estimatedw0^2],1/Fs);

% Estimativa do sinal de artefato
expectedNoise=lsim(estimatedTf,pureStimulation)';

% Sinal poluído
dirtySignal=cleanEEG+actualNoise;
% FFTs
dirtyFFT=fft(dirtySignal);
noiseFFT=fft(expectedNoise);

% Reconstrução
cleanReconstruction=ifft(dirtyFFT-noiseFFT);

%Erro de reconstrução
reconstructionError=cleanReconstruction-cleanEEG;
errorSquared=abs(reconstructionError);
errorSquared(isnan(errorSquared))=1e50;
qErrorSum=sum(errorSquared);
if(qErrorSum>maxError || isnan(qErrorSum))
   qErrorSum=maxError;
end

% Estimativa de SNRs
pre=snr_clean_reference(cleanEEG2,dirtySignal);
post=snr_clean_reference(cleanEEG2,cleanReconstruction);
referenceVsCleanSNR=snr_clean_reference(cleanEEG2,cleanEEG);
arr=real(post)/real(pre);
if(isnan(arr))
arr=-100;
end
% Plots
if(shouldPlot)
    disp(strcat('SNR Estimado Referencia/Limpo: ',sprintf('%.4f',referenceVsCleanSNR),'dB'));
    disp(strcat('SNR Estimado PRE: ',sprintf('%.4f',pre),'dB'));
    disp(strcat('SNR Estimado POST: ',sprintf('%.4f',post),'dB'));
    disp(strcat('Taxa de redução de artefato: ',sprintf('%.4f',arr)));
    disp(strcat('Soma do erro quadrático de reconstrução: ',sprintf('%.4f',qErrorSum)));

    figure(1),subplot(3,1,1), plot(dirtySignal),title('Sinal corrompido');
    figure(1),subplot(3,1,2), plot(cleanReconstruction),hold on,plot(cleanEEG),hold off,legend('recovered','original'),title('Reconstrução vs Sinal Limpo Original');
    figure(1),subplot(3,1,3), plot(reconstructionError),title('Erro de reconstrução');
end