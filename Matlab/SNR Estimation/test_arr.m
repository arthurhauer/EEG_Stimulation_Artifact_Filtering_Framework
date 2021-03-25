clear;
close all;
clc;

iterations=1000;
maxFs=2000;
minFs=100;
maxDuration=15;
minDuration=6;
maxFrequency=50;
minFrequency=1;
maxAmplitude=1;
minAmplitude=1;
maxSNR=0;
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
    frequency=[gen_rand_in_range(minFrequency,maxFrequency) gen_rand_in_range(minFrequency,maxFrequency)];
    amplitude=[gen_rand_in_range(minAmplitude,maxAmplitude) gen_rand_in_range(minAmplitude,maxAmplitude)];
    stimulation_artifact_SNR=gen_rand_in_range(minSNR,maxSNR);
    fsArray(i)=Fs;
    durationArray(i)=duration;
    frequencyArray(i)=abs(frequency(1)-frequency(2));
    amplitudeArray(i)=abs(amplitude(1)-amplitude(2));
    realSNR(i)=stimulation_artifact_SNR;
    [matlabEstimatedSNR(i),estimatedSNR(i)] = test_snr_estimation(Fs,duration,frequency,amplitude,stimulation_artifact_SNR,'clean',false);
end
elapsed=toc;

clear i Fs duration frequency amplitude stimulation_artifact_SNR;

error=realSNR-estimatedSNR;
absError=abs(error);

normError=normalize(error);
normRealSNR=normalize(realSNR);
normEstimatedSNR=normalize(estimatedSNR);
normMatlabEstimatedSNR=normalize(matlabEstimatedSNR);
normAmplitudeArray=normalize(amplitudeArray);
normFrequencyArray=normalize(frequencyArray);


figure(3), subplot(2,2,1),scatter(realSNR,error),title('SNR Real vs Erro'),xlabel('SNR Real'),ylabel('Erro');
figure(3), subplot(2,2,2),scatter(realSNR,estimatedSNR),title('SNR Real vs SNR Estimado'),xlabel('SNR Real'),ylabel('SNR Estimado');
figure(3), subplot(2,2,3),scatter(amplitudeArray,error),title('Diff Amplitude vs Erro'),xlabel('Diff Amplitude'),ylabel('Erro');
figure(3), subplot(2,2,4),histogram(error,100),title('Histograma do erro'),xlabel('dB'),ylabel('Frequência')

figure(4), scatter(frequencyArray,error),title('Diff Frequência vs Erro'),xlabel('Diff Frequência'),ylabel('Erro');

disp(strcat('Erro absoluto médio: ',sprintf('%.4f',mean(absError)),'dB'));
disp(strcat('Tempo total: ',sprintf('%.4f',elapsed),'segundos'));
disp(strcat('Tempo por iteração: ',sprintf('%.4f',elapsed/iterations),'segundos'));