%
% function [DataArtifact] = electricalstimartifactremoval(X,S,Fs,N,wiener_tupe,f1,f2,TW,ATT)
%
%   FILE NAME       : ELECTRICAL STIMULATION ARTIFACT REMOVAL
%   DESCRIPTION     : Generates a Wiener filter to predict and remove artifact
%                     from an electrical stimulation and neural recording session
%
%   X               : Matrix containing recorded channels - LxM (L=number
%                     of recorded channels; M = numbe of time samples)
%   S               : Matrix containing input stimulus - KxM (K = number of
%                     stimulation channels; M = number of time samples)
%   Fs              : Sampling rate in Hz
%   N               : Number of impulse response samples for Wiener filter
%                     calculation
%   wiener_analysis : Type of Wiener filter estimation procedure used
%                     'fft' : uses fft (frequency domain analysis) to estimate the filter, requires
%                     statistical independence between channels.
%                     'cov' : uses H = Cxx^-1 * Ryx to estimate the filter.
%                     Half the filter order.
%   f1              : Lower cutoff frequency (in Hz)
%   f2              : Upper cutoff frequency (in Hz)
%   TW              : Transition width (in Hz)
%   ATT             : Passband and stopband error (Attenuationin dB)
%
% RETURNED DATA
%
%  DataArtifact     : Data structure containing
%   
%   .X                  - Recorded data during stimulation
%   .S                  - Pulse sequence vector (or matrix) containing times 
%                         of electrical pulases. If electricaL stimulation
%                         is delivered across N channels in a stimulating
%                         array, then S is a matrix of dimnensoisn N x Nt
%                         where Nt is the number of tims samples
%   .Xpre               - Predicted electrical stimulation artifact
%   .Xclean             - Clean neural signal (X-Xpre)
%   .wiener_analysis    - Type of Wiener Filter estimation procedure
%   .wiener.N           - Wiener filter order 
%   .wiener.H           - Matrix H(k,l,:) containing the Wiener filters
%                         beteween the k-th input channel and l-th output
%                         channel. The third dimension has 2*N+1 time samples.
%   .f1                 - Lower cutoff frequency (in Hz)
%   .f2                 - Upper cutoff frequency (in Hz)
%   .TW                 - Transition width (in Hz)
%   .ATT                - Passband and stopband error (Attenuationin dB)
%   .Fs                 - Sampling rate (Hz)
%
% (C) Monty A. Escabi, Aug 2019 (Modified from ELECTRICALSTIMARTIFACTREMOVALTDT)
%
function [DataArtifact] = electricalstimartifactremoval(X,S,Fs,N,wiener_analysis,f1,f2,TW,ATT)

% %Some Parameters
NChanX=size(X,1);   %Number of output channels (recorded channels)
NChanS=size(S,1);   %Number of input channels (electrical stimulation channels)

%Filtering Darta if Desired
if nargin>5
    %Bandpass filter output
    [Hband] = bandpass(f1,f2,TW,Fs,ATT);
    Nb=(length(Hband)-1)/2;
    for l=1:NChanX
        X_temp(l,:)=conv(X(l,:),Hband);
    end
    X=X_temp(:,Nb+1:end-Nb);    %Removing filter delay
end

%Select the Wiener filter estimation procedure - uses either a covariance
%deconvolutation method or FFT based approach. FFT based approach requires
%that channels are independent of each other
if strcmp(wiener_analysis,'cov')
    
    %Finding Artifact Prediction Filters
    [H,~,~] = wienermimo(S,X,N);
    
    %Predicting Artifacts
    Nh = 2*N+1;         %Wiener Filter order for covariance calculation
    for l=1:NChanX      %output channels
        h=reshape(H(:,l),Nh,NChanS)';
        h=h(:,N+1:Nh);
        for k=1:NChanS  %input channels

            Ha(k,l,:)=h(k,:);           %Wiener Filter between the k-th input channel and l-th output channel
            Y=conv(S(k,:),squeeze(Ha(k,l,:)));
            Ya(l,k,:)=Y(1:end-N);       %Predicted artifacts for output channel l that arrises from input channel k
            
        end
    end
    
elseif strcmp(wiener_analysis,'fft')
    %Finding Artifact Prediction Filters
    for l=1:NChanX  %output channels
        for k=1:NChanS  %input channels
            [H] = wienerfft(S(k,:),X(l,:),0,N);
            Ha(k,l,:)=H;                %Wiener Filter between the k-th input channel and l-th output channel
        end
    end
    
    %Predicting Artifacts
    for l=1:NChanX  %output channels
        for k=1:NChanS  %input channels
            h(1,:)=Ha(k,l,:);
            Y=conv(S(k,:),h);
            Ya(l,k,:)=Y(1:end-N+1);     %Predicted artifacts for output channel l that arrises from input channel k

        end
    end
end

%Predicting Artifact and Subtracting
for l=1:NChanX  %output channels
    Xpre(l,:)=squeeze(sum(Ya(l,:,:),2))';   %Total Predicted artifact for each output channel - note that we need to sum the artifacts across all of the input channels
end
Xclean=X-Xpre;

%Organizing Results Into Data Structure
DataArtifact.X=X;
DataArtifact.S=S;
DataArtifact.Xpre=Xpre;   
DataArtifact.Xclean=Xclean;
DataArtifact.wiener.N=N;
DataArtifact.wiener.H=Ha;           %Wiener filter Matrix 
DataArtifact.Fs=Fs;
if nargin>5
    DataArtifact.BPF.f1=f1;
    DataArtifact.BPF.f2=f2;
    DataArtifact.BPF.TW=TW;
    DataArtifact.BPF.ATT=ATT;
end