%MULTI-CHANNEL ELETRICAL STIMULATION ARTIFACT REMOVAL EXAMPLE
%
%This is an example of artifact removal for multi-channel stimulation of IC
%while simulataneously recording neural activity in auditory cortex. The
%recording shows strong field potentials and there are some small
%multi-units signals (no single units are visible). The data for this
%example is the same as used for Fig. 5 of
%
%       Sadeghi et al. (2019) Optimal Multichannel Artifact Prediction and
%       Removal for Neural Stimulation and Brain Machine Interfaces. Front.
%       in Neurosci.
%
%The procedure generates a multi-input multi-output wiener filter that is
%used to predict artifacts across all output channels. The artifacts are
%then removed by subtraction.
%
%For this example the "input" is a multi-channel electrical stimulation signal
%
%       S - 16 input channels containing 2097152 time samples (16x2097152 matrix)
%
%The "output" is the recorded neural traces across 4 channels (obtained
%with a Neuronexus Q-trode). 
%
%       X - 4 recording channels containing 2097152 time samples (4x2097152 matrix)
%
%The procedure generates 64 filters (4x16; contained in DataArtifact.wiener.H, which
%are then used to predict the artifacts on X. The predicted artifacts for
%each of the four channels is in contained in the signal DataArtifact.Xpre
%
%The predicted artifacts are then removed by subtraction: X-Xpre. 
%
%The routine ELECTRICALSTIMARTIFACTREMOVAL carries out all of the above
%opreations. This is shown in the below example with and without filtering
%(filtering for spikes)
%

%Loading Raw Data
load DataArtifact16_Unfiltered.mat              %Unfiltered raw data
X=DataArtifact16_Unfiltered.Xa;                 %Matrix containging Recorded electrical stimulation on 4 channels (4 output chan x 2097152 time samples)
S=DataArtifact16_Unfiltered.Sa;                 %Matrix of Pulse train containing times of biphasic pulses across 16 chahnels (16 input chan x 2097152 time samples)
Fs=DataArtifact16_Unfiltered.Fs;                %Sampling Rate

%Removing Artifacts
f1=300;     %Filter Lower cutoff freq.
f2=5000;    %Filter Upper cutoff freq.
TW=200;     %Filter transition width
ATT=40;     %Filter attunenuation
N=40;       %Number of samples for Wiener filters
[DataArtifact] = electricalstimartifactremoval(X,S,12000,N,'cov');                     %Artifact removal using covariance Wiener filter estimation - no filtering
[DataArtifactF] = electricalstimartifactremoval(X,S,12000,N,'cov',f1,f2,TW,ATT);        %Artifact removal using covariance Wiener filter estimation - filtered for spikes between 300 and 5000 Hz

%Plotting original unfiltered Waveforms for channel 1 - recording was obtained with a
%neuronexus Q-Trode which has 4 channels
subplot(211)
N=size(DataArtifact.X,2);                       %Number of time samples
Fs=DataArtifact.Fs;                             %Sampling Rate
time=(1:N)/Fs;                                  %Time vector
plot(time,DataArtifact.X(1,:),'b')              %X is the recorded waveform  that contains artifact - note that it has 4 channels - dimensions 4xN
hold on
plot(time,DataArtifact.Xclean(1,:),'r')         %X is the recorded waveform  that contains artifact - note that it has 4 channels - dimensions 4xN
xlim([0 1])                                     %Display first 1 seconds
title('Unfiltered - Blue=original recording, Red=cleaned recording')

%Same as above except we are showing the filtered waveform -
%filtered between 300 - 5000 Hz
subplot(212)
N=size(DataArtifactF.X,2);                      %Number of time samples
Fs=DataArtifactF.Fs;                            %Sampling Rate
time=(1:N)/Fs;                                  %Time vector
plot(time,DataArtifactF.X(4,:),'b')             %X is the recorded waveform  that contains artifact - note that it has 4 channels - dimensions 4xN
hold on
plot(time,DataArtifactF.Xclean(4,:),'r')        %X is the recorded waveform  that contains artifact - note that it has 4 channels - dimensions 4xN
xlim([0 1])                                     %Display first 1 seconds
title('Filtered - Blue=original recording, Red=cleaned recording')
