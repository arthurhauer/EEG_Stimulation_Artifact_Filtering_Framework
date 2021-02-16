from Utils.utils import Utils
import statistics
import numpy
class ArtifactDetection:
#--------------------------------------------------------------------------------------------------#
#------------------------------------------- DOC---------------------------------------------------#
#--------------------------------------------------------------------------------------------------#

    """
    Class developed for detection of stimulus artifiact in EEG signals.
    Version: 1.0.1
    Authored by: Arthur Hauer
    Last modified: 16/02/2021
    """

#--------------------------------------------------------------------------------------------------#
#----------------------------------------- Fields--------------------------------------------------#
#--------------------------------------------------------------------------------------------------#

    eeg = [[]]
    n_samples=0

#--------------------------------------------------------------------------------------------------#
#-------------------------------------- Constructor------------------------------------------------#
#--------------------------------------------------------------------------------------------------#
    def __init__(self, eeg):
        """
        'eeg': 2D array, where the first index points to the channel, and the second index points to the timestamp.
        """
        self.eeg = eeg
        self.n_samples=len(eeg[0])

#--------------------------------------------------------------------------------------------------#
#----------------------------------- Private methods-----------------------------------------------#
#--------------------------------------------------------------------------------------------------#

    def __check_loaded_eeg(self):
        error=False
        try:
            error=len(self.eeg[0])<1
        except:
            error=True
        if(error):
            raise Exception('EEG not properly loaded.')

#--------------------------------------------------------------------------------------------------#
#----------------------------------- Public methods------------------------------------------------#
#--------------------------------------------------------------------------------------------------#

    def load_eeg(self,eeg:list):
        """
        Loads a new EEG reading.
        """
        self.eeg = eeg
        self.n_samples=len(eeg[0])

#--------------------------------------------------------------------------------------------------#

    def peak_detection(self,window_size:int, sensitivity:int, cluster_size:int) -> list:
        """
        Method based on the artifact detencion algorithm described on
        { 10.1109/IEMBS.2011.6091809: U. Hoffmann, W. Cho, A. Ramos-Murguialday, and T. Keller,
         “Detection and removal of stimulation artifacts in electroencephalogram
         recordings”,
         Proceedings of the Annual International Conference of the
         IEEE Engineering in Medicine and Biology Society,
         EMBS, pp. 7159–7162, 2011, Section III, Subsection A }.
         'eeg' parameter must be loaded before use.
        """
        # Check if loaded eeg is of valid format
        self.__check_loaded_eeg()

        # Compute first order differences between samples across channels
        first_order_diferences=Utils.first_order_differences(self.eeg)

        # Compute sliding windows median absolute deviation of first order differences
        median_absolute_deviation=Utils.sliding_median_absolute_deviation(first_order_diferences,window_size)

        # Initialize sensitivity factor
        sensitivity_multiplier=1/sensitivity

        # Initialize artifact location markings
        artifact_locations=[0]*self.n_samples

        last_detection=None
        for t in range(self.n_samples):
            # Set artifact location marking to 1 if first order difference of sample is greater than a scaled median absolute deviation for the same sample
            # Cluster detections
            artifact_locations[t]= 0 if abs(first_order_diferences[t])<sensitivity_multiplier*median_absolute_deviation[t] else 1
            if(artifact_locations[t]==1):
                if(cluster_size>0 and t>cluster_size):
                    if(numpy.amax(artifact_locations[t-cluster_size:t])>0):
                        artifact_locations[t-1]=1
                        artifact_locations[t-2]=1
                    if(last_detection!=None and t-last_detection<=cluster_size):
                        for i in range(t-last_detection,t):
                            artifact_locations[i]=1
                last_detection=t
        return artifact_locations

#--------------------------------------------------------------------------------------------------#

    def threshold(self,threshold:float,smoothing:int)->list:
        # Check if loaded eeg is of valid format
        self.__check_loaded_eeg()

        # Initialize artifact location markings
        artifact_locations=[0]*self.n_samples
        smooth=[0]*self.n_samples

        # Set artifact location marking to 1 if first order difference of sample is greater than a scaled median absolute deviation for the same sample
        for t in range(self.n_samples):
            artifact_locations[t]= 0 if abs(self.eeg[0][t])<threshold else 1

            if(t>smoothing and smoothing>0):
                avg=sum(artifact_locations[t-smoothing:t])/smoothing
                smooth[t] = 0 if avg<0.5 else 1
            else:
                smooth[t]=artifact_locations[t]

        return smooth

#--------------------------------------------------------------------------------------------------#
