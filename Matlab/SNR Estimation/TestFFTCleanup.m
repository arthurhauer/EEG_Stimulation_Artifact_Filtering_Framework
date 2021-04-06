clear;
close all;
clc;

iterations=1000;
maxFs=500;
minFs=500;
maxDuration=15;
minDuration=15;
maxFrequency=50;
minFrequency=50;
maxAmplitude=1;
minAmplitude=1;
maxpreSNR=100;
minpreSNR=100;
maxpostSNR=100;
minpostSNR=100;
maxZetaError=0.000001;
minZetaError=-0.000001;
maxw0Error=0.1*pi/180;
minw0Error=-0.1*pi/180;

arrArray=zeros(iterations,1);
qErrorSumArray=zeros(iterations,1);
zetaErrorArray=zeros(iterations,1);
w0ErrorArray=zeros(iterations,1);

tic;
parfor i=1:iterations
    Fs=gen_rand_in_range(minFs,maxFs);
    duration=gen_rand_in_range(minDuration,maxDuration);
    frequency=[gen_rand_in_range(minFrequency,maxFrequency) gen_rand_in_range(minFrequency,maxFrequency) gen_rand_in_range(minFrequency,maxFrequency)];
    amplitude=[gen_rand_in_range(minAmplitude,maxAmplitude) gen_rand_in_range(minAmplitude,maxAmplitude) gen_rand_in_range(minAmplitude,maxAmplitude)];
    preSNR=gen_rand_in_range(minpreSNR,maxpreSNR);
    postSNR=gen_rand_in_range(minpostSNR,maxpostSNR);
    zetaError=gen_rand_in_range(minZetaError,maxZetaError);
    w0Error=gen_rand_in_range(minw0Error,maxw0Error);
    
    zetaErrorArray(i)=zetaError;
    w0ErrorArray(i)=w0Error;
    
    [qErrorSumArray(i),arrArray(i)] = tf_estimation_cleanup(frequency,duration,amplitude,Fs,zetaError,w0Error,preSNR,postSNR,false);
end
elapsed=toc;

clear i Fs duration frequency amplitude preSNR postSNR zetaError w0Error;

normError=normalize(qErrorSumArray);
normArr=normalize(abs(arrArray));
normZetaError=normalize(zetaErrorArray);
normW0Error=normalize(w0ErrorArray);

figure(1), subplot(2,1,1), scatter3(normError,normZetaError,normW0Error),title('Soma do erro quadrático vs Erro de estimativa'),xlabel('Erro quadrático'),ylabel('Erro Zeta'),zlabel('Erro W0');
figure(1), subplot(2,1,2), scatter3(normArr,normZetaError,normW0Error),title('Artifact Reduction Ratio vs Erro de estimativa'),xlabel('ARR'),ylabel('Erro Zeta'),zlabel('Erro W0');

disp(strcat('Tempo total: ',sprintf('%.4f',elapsed),'segundos'));
disp(strcat('Tempo por iteração: ',sprintf('%.4f',elapsed/iterations),'segundos'));