function [ realSNR,meanSNR ] = test_snr_estimation( Fs,duration,frequency,amplitude,stimulation_artifact_SNR,method,shouldPlot)

acquisitions=2;    

[basisSignal,t]=generate_sine_wave(frequency(1),duration,amplitude(1),Fs); % Generate sinewave
cleanSignal=zeros(10,size(t,2));
dirtySignal=zeros(10,size(t,2));
for i=1:acquisitions
    parameterIndex=1;
   if(strcmp(method,'clean'))
       parameterIndex=i;
   end
   [basisSignal,t]=generate_sine_wave(frequency(parameterIndex),duration,amplitude(parameterIndex),Fs); % Generate sinewave
   cleanSignal(i,:)= awgn(basisSignal,5,'measured'); % Add white gaussian noise to act as commonly found noise in measurements
   dirtySignal(i,:)=generate_repeatable_awgn(cleanSignal(i,:),stimulation_artifact_SNR);% Add stimulation artifact noise
end
noise=dirtySignal(1,:)-cleanSignal(1,:);
totalComparisons=((acquisitions-1+1)*(acquisitions-1))/2;
estimatedSNRArray=zeros(totalComparisons,1);
for i=1:acquisitions-1
    for j=i:acquisitions
        if(strcmp(method,'clean'))
            estimatedSNRArray(i)=10*log10(sum(cleanSignal(j,:).^2)/sum((dirtySignal(i,:)-cleanSignal(j,:)).^2));
        else if(strcmp(method,'cpsd'))
                [cleanEstimatedSNR,f]=snr_estimation(cleanSignal(i,:),cleanSignal(j,:),Fs); % Estimate 'dirty' signal's SNR
                [estimatedSNR,f]=snr_estimation(dirtySignal(i,:),dirtySignal(j,:),Fs); % Estimate 'dirty' signal's SNR
                estimatedSNRArray(i)= abs(10*log10(nanmean(cleanEstimatedSNR)))-abs(10*log10(nanmean(estimatedSNR)));
            end
        end
    end
end

meanSNR = mean(estimatedSNRArray);
realSNR = snr(dirtySignal(1,:),noise);

if(shouldPlot)
    figure(1),subplot(2,2,1),plot(t,basisSignal(1,:)),title('Sinal base');
    figure(1),subplot(2,2,2),plot(t,cleanSignal(1,:)),title('Sinal sem estímulo');
    figure(1),subplot(2,2,3),plot(t,dirtySignal(1,:)),title('Sinal com estímulo');
    figure(1),subplot(2,2,4),plot(t,noise),title('Ruido');
end

end

