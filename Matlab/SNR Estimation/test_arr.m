clear;
close all;
clc;

iterations=5000;
maxFs=2000;
minFs=100;
maxDuration=6;
minDuration=15;
maxFrequency=50;
minFrequency=1;
maxAmplitude=5;
minAmplitude=0.1;
maxSNR=1;
minSNR=0.1;

estimatedSNR=zeros(iterations,1);
realSNR=zeros(iterations,1);
fsArray=zeros(iterations,1);
durationArray=zeros(iterations,1);
frequencyArray=zeros(iterations,1);
amplitudeArray=zeros(iterations,1);
snrArray=zeros(iterations,1);
tic;
for i=1:iterations
    Fs=gen_rand_in_range(minFs,maxFs);
    duration=gen_rand_in_range(minDuration,maxDuration);
    frequency=gen_rand_in_range(minFrequency,maxFrequency);
    amplitude=gen_rand_in_range(minAmplitude,maxAmplitude);
    stimulation_artifact_SNR=gen_rand_in_range(minSNR,maxSNR);
    fsArray(i)=Fs;
    durationArray(i)=duration;
    frequencyArray(i)=frequency;
    amplitudeArray(i)=amplitude;
    snrArray(i)=stimulation_artifact_SNR;
    [realSNR(i),estimatedSNR(i)] = test_snr_estimation(Fs,duration,frequency,amplitude,stimulation_artifact_SNR);
end
elapsed=toc;

clear i Fs duration frequency amplitude stimulation_artifact_SNR;

figure(1), plot(realSNR,'--'),xlabel('Itera��o'),ylabel('dB');
hold on;
plot(estimatedSNR);
hold off;
legend('SNR Real','SNR Estimado')

error=realSNR-estimatedSNR;
absError=abs(error);

figure(2), subplot(3,1,1),plot(absError),title('Erro'),ylabel('dB');
figure(2), subplot(3,1,3),histogram(error,100),title('Histograma do erro'),xlabel('dB'),ylabel('Frequ�ncia')
figure(2), subplot(3,1,2),plot(absError),title('Erro absoluto'),ylabel('dB');

figure(3), subplot(3,1,1),scatter(snrArray,error),title('SNR (par�metro) vs Erro'),xlabel('SNR (par�metro)'),ylabel('Erro');
figure(3), subplot(3,1,2),scatter(snrArray,realSNR),title('SNR (par�metro) vs SNR Real'),xlabel('SNR (par�metro)'),ylabel('SNR Real');
figure(3), subplot(3,1,3),scatter(snrArray,error),title('SNR (par�metro) vs SNR Estimado'),xlabel('SNR (par�metro)'),ylabel('SNR Estimado');

disp(strcat('Erro absoluto m�dio: ',sprintf('%.4f',mean(absError)),'dB'));
disp(strcat('Tempo total: ',sprintf('%.4f',elapsed),'segundos'));
disp(strcat('Tempo por itera��o: ',sprintf('%.4f',elapsed/iterations),'segundos'));