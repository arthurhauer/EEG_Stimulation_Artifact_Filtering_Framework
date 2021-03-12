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
maxSNR=100;
minSNR=-100;

estimatedSNR=zeros(iterations,1);
matlabEstimatedSNR=zeros(iterations,1);
fsArray=zeros(iterations,1);
durationArray=zeros(iterations,1);
frequencyArray=zeros(iterations,1);
amplitudeArray=zeros(iterations,1);
realSNR=zeros(iterations,1);
tic;
parfor i=1:iterations
    Fs=gen_rand_in_range(minFs,maxFs);
    duration=gen_rand_in_range(minDuration,maxDuration);
    frequency=gen_rand_in_range(minFrequency,maxFrequency);
    amplitude=gen_rand_in_range(minAmplitude,maxAmplitude);
    stimulation_artifact_SNR=gen_rand_in_range(minSNR,maxSNR);
    fsArray(i)=Fs;
    durationArray(i)=duration;
    frequencyArray(i)=frequency;
    amplitudeArray(i)=amplitude;
    realSNR(i)=stimulation_artifact_SNR;
    [matlabEstimatedSNR(i),estimatedSNR(i)] = test_snr_estimation(Fs,duration,frequency,amplitude,stimulation_artifact_SNR);
end
elapsed=toc;

clear i Fs duration frequency amplitude stimulation_artifact_SNR;

error=realSNR-estimatedSNR;
absError=abs(error);

normError=normalize(error);
normRealSNR=normalize(realSNR);
normEstimatedSNR=normalize(estimatedSNR);
normMatlabEstimatedSNR=normalize(matlabEstimatedSNR);

% figure(1), plot(realSNR,'--'),xlabel('Iteração'),ylabel('dB');
% hold on;
% plot(estimatedSNR);
% hold off;
% legend('SNR Real','SNR Estimado')
% 
% 
% figure(2), subplot(3,1,1),plot(absError),title('Erro'),ylabel('dB');
% figure(2), subplot(3,1,2),plot(absError),title('Erro absoluto'),ylabel('dB');

figure(3), subplot(2,2,1),scatter(normRealSNR,normError),title('SNR Real vs Erro'),xlabel('SNR Real'),ylabel('Erro');
figure(3), subplot(2,2,2),scatter(normRealSNR,normEstimatedSNR),title('SNR Real vs SNR Estimado'),xlabel('SNR Real'),ylabel('SNR Estimado');
figure(3), subplot(2,2,3),scatter(normRealSNR,normMatlabEstimatedSNR),title('SNR Real vs SNR Estimado (Matlab)'),xlabel('SNR Estimado'),ylabel('Erro');
figure(3), subplot(2,2,4),histogram(error,100),title('Histograma do erro'),xlabel('dB'),ylabel('Frequência')

disp(strcat('Erro absoluto médio: ',sprintf('%.4f',mean(absError)),'dB'));
disp(strcat('Tempo total: ',sprintf('%.4f',elapsed),'segundos'));
disp(strcat('Tempo por iteração: ',sprintf('%.4f',elapsed/iterations),'segundos'));