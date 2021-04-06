%EXAMPLE COCHLEAR IMPLANT RECORDING WITH ARTIFACT REMOVAL
%
%This an artifact removal example for binaural stimulation using
%cochlear implants in rat whie simulatenously recording from inferior
%colliculus. The recording was performed in Dr. Jan Schnup's laboratory 
%(City Univ. of Hong Kong) using a 32 channel neuronexus recording array. 
%In this example, only two channnels that contained well isolated single 
%units are provided.
%
%The stimulus current used for this example consisted of a binaural cosine
%ramped click train as shown in Fig. 3 of
%
%       Sadeghi et al. (2019) Optimal Multichannel Artifact Prediction and
%       Removal for Neural Stimulation and Brain Machine Interfaces. Front.
%       in Neurosci.
%
%For this example the "input" is a two-channel electrical stimulation
%signal (i.e., binaural input)
%
%       S - 2 input channels containing 1079910 time samples (2x1079910 matrix)
%
%The inputs are represented as a time-series of pulses where the amplitude
%of each pulse is proportional to the amplitude of the delivered
%by-phasic current (normalized for a maximum value of 1). 
%
%The "output" is the recorded neural traces on two channels.
%
%       X - 2 recording channels containing 1079910 time samples (2x1079910 matrix)
%
%The first recording channel ( X(1,:) ) contains the neural data for
%Fig. 3 in Sadeghi et al.
%
%The procedure generates filters (contained in DataArtifact.wiener.H, which
%are then used to predict the artifacts on X. The predicted artifacts for
%each of the four channels is in contained in the signal DataArtifact.Xpre.
%
%The predicted artifacts are then removed by subtraction: X-Xpre. 
%
%The routine ELECTRICALSTIMARTIFACTREMOVAL carries out all of the above
%opreations. This is shown in the below example with and without filtering
%(filtering for spikes)
%

%Loading Raw Data
load BinauralCIExample.mat                      %Unfiltered raw data

%Removing Artifacts
f1=300;     %Filter Lower cutoff freq.
f2=10000;   %Filter Upper cutoff freq.
TW=100;     %Filter transition width
ATT=40;     %Filter attunenuation
N=40;       %Number of samples for Wiener filters
[DataArtifact] = electricalstimartifactremoval(X,S,Fs,N,'cov',f1,f2,TW,ATT);        %Artifact removal using covariance Wiener filter estimation - filtered for spikes between 300 and 5000 Hz

%Plotting original Waveforms and Cleaned Waveforms for the first recording channel
subplot(211)
N=size(DataArtifact.X,2);                       %Number of time samples
Fs=DataArtifact.Fs;                             %Sampling Rate
time=(1:N)/Fs;                                  %Time vector
plot(time,DataArtifact.X(1,:),'k')              %X is the recorded waveform  that contains artifact - showing channel 1
hold on
plot(time,DataArtifact.Xclean(1,:),'r')         %X is the clean waveform  that contains artifact - showing channel 1
title('Black=original recording, Red=cleaned recording')

%Plotting original Waveforms and Cleaned Waveforms for the second recording channel
subplot(212)
N=size(DataArtifact.X,2);                       %Number of time samples
Fs=DataArtifact.Fs;                             %Sampling Rate
time=(1:N)/Fs;                                  %Time vector
plot(time,DataArtifact.X(2,:),'k')              %X is the recorded waveform  that contains artifact - showing channel 2
hold on
plot(time,DataArtifact.Xclean(2,:),'r')         %X is the clean waveform  that contains artifact - showing channel 2
title('Black=original recording, Red=cleaned recording')


