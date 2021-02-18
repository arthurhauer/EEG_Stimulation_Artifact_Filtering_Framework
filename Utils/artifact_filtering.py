from Utils.artifact_detection import ArtifactDetection
import copy
class ArtifactFiltering:
#--------------------------------------------------------------------------------------------------#
#------------------------------------------- DOC---------------------------------------------------#
#--------------------------------------------------------------------------------------------------#

    """
    Class developed for filtering of stimulus artifiact in EEG signals.
    Version: 1.0.0
    Last modified by: Arthur Hauer
    Last modification date: 18/02/2021
    """

#--------------------------------------------------------------------------------------------------#
#----------------------------------------- Fields--------------------------------------------------#
#--------------------------------------------------------------------------------------------------#

    eeg = [[]]
    stimulation_markings=[]
    n_samples=0

    def __init__(self, eeg:list,stimulation_markings:list=[]):
        print('Init Artifact Filtering Class')
        self.eeg = eeg
        self.n_samples=len(eeg[0])
        self.stimulation_markings

    def __get_eeg_copy(self)->list:
        return copy.deepcopy(self.eeg)

    def __check_loaded_eeg(self):
        error=False
        try:
            error=len(self.eeg[0])<1
        except:
            error=True
        if(error):
            raise Exception('EEG not properly loaded.')

    def __check_loaded_markings(self):
        error=False
        try:
            error=len(self.stimulation_markings)<1
        except:
            error=True
        if(error):
            raise Exception('Stimulation markings not properly loaded.')

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

    def load_eeg(self, eeg:list):
        self.eeg=eeg
        self.n_samples=len(eeg[0])

    def load_stimulation_markings(self,stimulation_markings:list):
        self.stimulation_markings=stimulation_markings


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

    def get_eeg(self)->list:
        self.__check_loaded_eeg()
        return self.eeg

    def get_stimulation_markings(self)->list:
        self.__check_loaded_markings()
        return self.stimulation_markings

    def template_subtraction(self):
        raise Exception("Not Implemented")

    def reference_signal_subtraction(self):
        raise Exception("Not Implemented")

    def blanking_interpolation(self)->list:
        """
        Method based on the eeg stimulation artifact blanking and interpolation algorithm described on
        { 10.1109/IEMBS.2011.6091809: U. Hoffmann, W. Cho, A. Ramos-Murguialday, and T. Keller,
         “Detection and removal of stimulation artifacts in electroencephalogram
         recordings”,
         Proceedings of the Annual International Conference of the
         IEEE Engineering in Medicine and Biology Society,
         EMBS, pp. 7159–7162, 2011, Section III, Subsection B }.
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
            ts=indexes[i]-1
            te=indexes[i]+lengths[i]
            for t in range(ts,te):
                for channel in range(len(self.eeg)):
                    filtered_signal[channel][t]=((self.eeg[channel][te]*(t-ts))/(te-ts))+((self.eeg[channel][ts]*(te-t))/(te-ts))

        return filtered_signal

    def blanking_gaussian_distribution(self):
        raise Exception("Not Implemented")

    def common_average_reference(self):
        raise Exception("Not Implemented")

    def linear_regression_reference(self):
        raise Exception("Not Implemented")

    def sys_id_wiener_filtering(self):
        raise Exception("Not Implemented")
