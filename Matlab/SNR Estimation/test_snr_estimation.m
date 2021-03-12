function [ realMeanSNR,estimatedMeanSNR ] = test_snr_estimation( Fs,duration,frequency,amplitude,stimulation_artifact_SNR,showPlots )
if nargin>5
        shouldPlot=showPlots;
    else if nargin==5
        shouldPlot=false;
        else
            error('Número inválido de parâmetros');
            return
        end
    end

[basisSignal,t]=generate_sine_wave(frequency,duration,amplitude,Fs); % Generate sinewave

cleanSignal1=awgn(basisSignal,10,'measured'); % Add white gaussian noise to act as commonly found noise in measurements
cleanSignal2=awgn(basisSignal,10,'measured');

signal1=generate_repeatable_awgn(cleanSignal1,stimulation_artifact_SNR);% Add stimulation artifact noise
signal2=generate_repeatable_awgn(cleanSignal2,stimulation_artifact_SNR);
noise=signal1-cleanSignal1;

[estimatedCleanSNR,f]=snr_estimation(cleanSignal1,cleanSignal2,Fs); % Estimate 'dirty' signal's SNR
[estimatedSNR,f]=snr_estimation(signal1,signal2,Fs); % Estimate 'dirty' signal's SNR

meanCleanSNR = 10*log10(mean(estimatedCleanSNR));
meanSNR = 10*log10(mean(estimatedSNR));
realMeanSNR = snr(signal1,noise);
estimatedMeanSNR=abs(meanCleanSNR)-abs(meanSNR);

if shouldPlot
    figure(1),subplot(2,1,1),plot(t,cleanSignal1),title('Sinal limpo 1')
    figure(1),subplot(2,1,2),plot(t,cleanSignal2),title('Sinal limpo 2')
    figure(2),subplot(3,1,1),plot(t,signal1),title('Sinal sujo 1')
    figure(2),subplot(3,1,2),plot(t,signal2),title('Sinal sujo 2')
    figure(2),subplot(3,1,3),plot(t,noise),title('Ruído')
    figure(3),
    subplot(2,1,1),
    plot(f,10*log10(estimatedCleanSNR)),
    title(strcat('Clean Signal SNR: ',sprintf('%.4f',meanCleanSNR),'dB')),
    ylabel('Power/frequency (dB/Hz)'),
    xlabel('Frequency (Hz)'),
    grid on;
    figure(3),
    subplot(2,1,2),
    plot(f,10*log10(estimatedSNR)),
    title(strcat('Artifact Signal SNR: ',sprintf('%.4f',meanSNR),'dB')),
    ylabel('Power/frequency (dB/Hz)'),
    xlabel('Frequency (Hz)'),
    grid on;
    disp(strcat('Estimated SNR: ',sprintf('%.4f',estimatedMeanSNR),'dB'));
    disp(strcat('Real Mean SNR: ',sprintf('%.4f',realMeanSNR),'dB'));
end

end

