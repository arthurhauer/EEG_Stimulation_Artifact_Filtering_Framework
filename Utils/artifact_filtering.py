from Utils.artifact_detection import ArtifactDetection
import numpy as np
import copy

class ArtifactFiltering:
#--------------------------------------------------------------------------------------------------#
#------------------------------------------- DOC---------------------------------------------------#
#--------------------------------------------------------------------------------------------------#

    """
    Class developed for filtering of stimulus artifiact in EEG signals.
    Version: 1.0.1
    Last modified by: Arthur Hauer
    Last modification date: 25/02/2021
    """

#--------------------------------------------------------------------------------------------------#
#----------------------------------------- Fields--------------------------------------------------#
#--------------------------------------------------------------------------------------------------#

    eeg = [[]]
    stimulation_markings=[]
    n_samples=0

#--------------------------------------------------------------------------------------------------#
#-------------------------------------- Constructor------------------------------------------------#
#--------------------------------------------------------------------------------------------------#

    def __init__(self, eeg:list,stimulation_markings:list=[]):
        print('Init Artifact Filtering Class')
        self.eeg = eeg
        self.n_samples=len(eeg)
        self.stimulation_markings

#--------------------------------------------------------------------------------------------------#
#----------------------------------- Private methods-----------------------------------------------#
#--------------------------------------------------------------------------------------------------#

    def __get_eeg_copy(self)->list:
        return copy.deepcopy(self.eeg)

#--------------------------------------------------------------------------------------------------#

    def __check_signal(self,signal:list):
        error=False
        try:
            error=len(signal)<1
        except:
            error=True
        if(error):
            raise Exception('Signal not properly loaded.')

#--------------------------------------------------------------------------------------------------#

    def __check_loaded_eeg(self):
        try:
            self.__check_eeg(self.eeg)
        except:
            raise Exception('EEG not properly loaded')

#--------------------------------------------------------------------------------------------------#

    def __check_loaded_markings(self):
        try:
            self.__check_eeg(self.stimulation_markings)
        except:
            raise Exception('Stimulation markings not properly loaded.')
            

#--------------------------------------------------------------------------------------------------#

    def __blank_artifacts(self)->(list,list):

        indexes=[]
        lengths=[]
        currentLength=0
        markingMemory=False
        currentMarking=False

        for t in range(self.n_samples):

            currentMarking=self.stimulation_markings[t]==1

            # Current index is marked as artifact
            if currentMarking:
                # Rising edge, means we should store the current index and reset de artifact length variable
                if not markingMemory:
                    indexes.append(t)
                    currentLength=0
                # As there's still artifact, increment artifact length
                currentLength+=1

            # Current index is marked as good signal
            else:
                # Falling edge, means we should store the artifact length
                if markingMemory:
                    lengths.append(currentLength)
            
            # Store the current marking value for evaluating falling or rising edge conditions on the next iteration
            markingMemory=currentMarking

        indexes_size=len(indexes)
        lengths_size=len(lengths)

        if indexes_size != lengths_size:
            raise Exception("Lists size mismatch!")
        else:
            return indexes,lengths

#--------------------------------------------------------------------------------------------------#
#----------------------------------- Public methods------------------------------------------------#
#--------------------------------------------------------------------------------------------------#

    def load_eeg(self, eeg:list):
        self.eeg=eeg
        self.n_samples=len(eeg)

#--------------------------------------------------------------------------------------------------#

    def load_stimulation_markings(self,stimulation_markings:list):
        self.stimulation_markings=stimulation_markings

#--------------------------------------------------------------------------------------------------#

    def generate_stimulation_markings(self,method:str='peak_detection',**kwargs):
        try:
            cluster_size=kwargs.get('cluster_size')
        except:
            cluster_size=200
        detection=ArtifactDetection(self.eeg,cluster_size)
        if method=='peak_detection':
            try:
                window_size=kwargs.get('window_size')
                sensitivity=kwargs.get('sensitivity')
            except:
                window_size=25
                sensitivity=3
            self.stimulation_markings=detection.peak_detection(window_size,sensitivity)

        elif method=='threshold':
            try:
                threshold=kwargs.get('threshold')
            except:
                threshold=250
            self.stimulation_markings=detection.threshold(threshold)
        else:
            raise Exception("Detection method invalid!")

#--------------------------------------------------------------------------------------------------#

    def get_eeg(self)->list:
        self.__check_loaded_eeg()
        return self.eeg

#--------------------------------------------------------------------------------------------------#

    def get_stimulation_markings(self)->list:
        self.__check_loaded_markings()
        return self.stimulation_markings

#--------------------------------------------------------------------------------------------------#

    def template_subtraction(self):
        raise Exception("Not Implemented")

#--------------------------------------------------------------------------------------------------#

    def reference_signal_subtraction(self):
        raise Exception("Not Implemented")

#--------------------------------------------------------------------------------------------------#

    def blanking(self)->list:
        """
        Method based on the eeg blanking algorithm described on
        { J. S. Lewis, Z. Barani, A. S. Magana, and F. Kargar,
         “Signal processing methods for reducing artifacts in microelectrode brain recordings causedby functional electrical stimulation,”
          pp. 0–31, 2019 }.
        This method assumes the entire corrupted signal is unusable, and should be excluded
         'eeg' parameter must be loaded before use.
        """
        # Check if loaded eeg is of valid format
        self.__check_loaded_eeg()

        # Check if loaded stimulation markings is valid
        try:
            self.__check_loaded_markings()
        # If markings are invalid, generate markings with the default method
        except:
            self.generate_stimulation_markings('peak_detection', window_size=25,sensitivity=3)
        
        (indexes,lengths)=self.__blank_artifacts()

        filtered_signal=self.__get_eeg_copy()

        for i in range(len(indexes)):
            filtered_signal[i:i+lengths[i]]=[0]*lengths[i]
        return filtered_signal

#--------------------------------------------------------------------------------------------------#

    def blanking_interpolation(self)->list:
        """
        Method based on the eeg stimulation artifact blanking and interpolation algorithm described on
        { 10.1109/IEMBS.2011.6091809: U. Hoffmann, W. Cho, A. Ramos-Murguialday, and T. Keller,
         “Detection and removal of stimulation artifacts in electroencephalogram
         recordings”,
         Proceedings of the Annual International Conference of the
         IEEE Engineering in Medicine and Biology Society,
         EMBS, pp. 7159–7162, 2011, Section III, Subsection B }.
         This method assumes the entire corrupted signal is unusable, and should be replaced by a linear interpolation between the sample the precedes the artifact and the sample comes right after it.
         'eeg' parameter must be loaded before use.
        """
        # Check if loaded eeg is of valid format
        self.__check_loaded_eeg()

        # Check if loaded stimulation markings is valid
        try:
            self.__check_loaded_markings()
        # If markings are invalid, generate markings with the default method
        except:
            self.generate_stimulation_markings('peak_detection', window_size=25,sensitivity=3)
        
        (indexes,lengths)=self.__blank_artifacts()

        filtered_signal=self.__get_eeg_copy()

        for i in range(len(indexes)):
            ts=indexes[i]-1 if indexes[i]>0 else 0
            te=indexes[i]+lengths[i]
            for t in range(ts,te):
                for channel in range(len(self.eeg[0])):
                    filtered_signal[t][channel]=((self.eeg[te][channel]*(t-ts))/(te-ts))+((self.eeg[ts][channel]*(te-t))/(te-ts))

        return filtered_signal

#--------------------------------------------------------------------------------------------------#

    def blanking_gaussian_distribution(self,artifact_free_data:list,training_vector_samples:int):
        """
        Method based on the eeg stimulation artifact blanking and interpolation algorithm described on
        { 10.1109/IEMBS.2011.6091809: U. Hoffmann, W. Cho, A. Ramos-Murguialday, and T. Keller,
         “Detection and removal of stimulation artifacts in electroencephalogram
         recordings”,
         Proceedings of the Annual International Conference of the
         IEEE Engineering in Medicine and Biology Society,
         EMBS, pp. 7159–7162, 2011, Section III, Subsection C }.
         This method assumes the entire corrupted signal is unusable, and should be replaced by the most probable signal based on training.
         'eeg' parameter must be loaded before use.
        """
        # Check if loaded eeg is of valid format
        self.__check_loaded_eeg()

        # Check if loaded training data is of valid format
        try:
            self.__check_signal(artifact_free_data)
        except:
            raise Exception("Artifact free training data not properly loaded.")

        # Check if loaded stimulation markings is valid
        try:
            self.__check_loaded_markings()
        # If markings are invalid, generate markings with the default method
        except:
            self.generate_stimulation_markings('peak_detection', window_size=25,sensitivity=3)
        
        # Get artifacts indexes and duration in samples
        (indexes,lengths)=self.__blank_artifacts()

        # Copy training data to avoid messing with the original object
        training_data=copy.deepcopy(artifact_free_data)

        # Copy eeg data to avoid messing with the original object
        filtered_signal=self.__get_eeg_copy()

        # Normalize by subtracting the mean in each channel, and set the variance of each channel to 1

        #TODO Implementar normalização

        # Form column vectors of dimension {training_vector_samples}*{n_channels} X 1 from the normalized multichannel segments

        z = np.array([[]])

        # Number of training vectors

        N = len(z)

        # Sample mean

        m = 1/N*sum(z)

        # Covariance matrix
        summed=0
        for zi in z:
            summed+=np.array(zi-m).transpose()*(zi-m)
        E=1/N*summed

        #TODO Falta conhecimento para implementar a parte seguinte!
        
        return filtered_signal

#--------------------------------------------------------------------------------------------------#

    def common_average_reference(self):
        """
        Method based on the eeg common average reference algorithm described on
        { J. S. Lewis, Z. Barani, A. S. Magana, and F. Kargar,
         “Signal processing methods for reducing artifacts in microelectrode brain recordings causedby functional electrical stimulation,”
          pp. 0–31, 2019 }.
        This method assumes the artifact is similar across all channels, and can be predicted by a fixed average.
         'eeg' parameter must be loaded before use.
        """

#--------------------------------------------------------------------------------------------------#

    def linear_regression_reference(self):
        """
        Method based on the eeg linear regression reference algorithm described on
        { J. S. Lewis, Z. Barani, A. S. Magana, and F. Kargar,
         “Signal processing methods for reducing artifacts in microelectrode brain recordings causedby functional electrical stimulation,”
          pp. 0–31, 2019 }.
        This method assumes the artifact is similar across some channels, and can be predicted by a weighted sum of other channels.
         'eeg' parameter must be loaded before use.
        """

#--------------------------------------------------------------------------------------------------#

    def sys_id_wiener_filtering(self):
         """
        Method based on the eeg linear regression reference algorithm described on
        { M.  Sadeghi  Najafabadi,  L.  Chen,  K.  Dutta,  A.  Norris,  B.  Feng,  J.  W.Schnupp, N. Rosskothen-Kuhl, H. L. Read, and M. A. Escabí,
         “OptimalMultichannel  Artifact  Prediction  and  Removal  for  Neural  Stimulationand  Brain  Machine  Interfaces”,
         Frontiers  in  Neuroscience,
         vol.  14,  no.July, pp. 1–19, 2020. }.
        This method assumes the artifact has a linear relation with the stimulation current, and can be predicted through system identification.
         'eeg' parameter must be loaded before use.
        """

#--------------------------------------------------------------------------------------------------#