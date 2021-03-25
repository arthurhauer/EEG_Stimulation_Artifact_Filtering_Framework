function [ realSNR,meanSNR ] = test_snr_estimation( Fs,duration,frequency,amplitude,stimulation_artifact_SNR,method)
if nargin>5
    if(~strcmp(chosen,'clean') && ~strcmp(chosen,'cspd'))
        error('M�todo inv�lido.');
        return
    end
    chosen=method;
else if nargin==5
        chosen='clean';
      else
        error('N�mero inv�lido de par�metros');
        return
     end
end

acquisitions=2;    

[basisSignal,t]=generate_sine_wave(frequency,duration,amplitude,Fs); % Generate sinewave
cleanSignal=zeros(10,size(t,2));
dirtySignal=zeros(10,size(t,2));
for i=1:acquisitions
   if(strcmp(chosen,'clean'))
       frequency=frequency+5;
       amplitude=amplitude+2;
   end
   [basisSignal,t]=generate_sine_wave(frequency,duration,amplitude,Fs); % Generate sinewave
   cleanSignal(i,:)= awgn(basisSignal,20,'measured'); % Add white gaussian noise to act as commonly found noise in measurements
   dirtySignal(i,:)=generate_repeatable_awgn(cleanSignal(i,:),stimulation_artifact_SNR);% Add stimulation artifact noise
end
noise=dirtySignal(1,:)-cleanSignal(1,:);
totalComparisons=((acquisitions-1+1)*(acquisitions-1))/2;
estimatedSNRArray=zeros(totalComparisons,1);
for i=1:acquisitions-1
    for j=i:acquisitions
        if(strcmp(chosen,'clean'))
            estimatedSNRArray(i)=10*log10(sum(cleanSignal(j,:).^2)/sum((dirtySignal(i,:)-cleanSignal(j,:)).^2));
        else if(strcmp(chosen,'cpsd'))
                [cleanEstimatedSNR,f]=snr_estimation(cleanSignal(i,:),cleanSignal(j,:),Fs); % Estimate 'dirty' signal's SNR
                [estimatedSNR,f]=snr_estimation(dirtySignal(i,:),dirtySignal(j,:),Fs); % Estimate 'dirty' signal's SNR
                estimatedSNRArray(i)= abs(10*log10(nanmean(cleanEstimatedSNR)))-abs(10*log10(nanmean(estimatedSNR)));
            end
        end
    end
end

meanSNR = mean(estimatedSNRArray);
realSNR = snr(dirtySignal(1,:),noise);

end

