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
    Last modified by: Arthur Hauer
    Last modification date: 16/02/2021
    """

#--------------------------------------------------------------------------------------------------#
#----------------------------------------- Fields--------------------------------------------------#
#--------------------------------------------------------------------------------------------------#

    eeg = [[]]
    n_samples=0
    cluster_size=0

#--------------------------------------------------------------------------------------------------#
#-------------------------------------- Constructor------------------------------------------------#
#--------------------------------------------------------------------------------------------------#

    def __init__(self, eeg:list,cluster_size:int=0):
        """
        'eeg': 2D array, where the first index points to the channel, and the second index points to the timestamp.
        """
        self.eeg = eeg
        self.n_samples=len(eeg)
        self.cluster_size=cluster_size

#--------------------------------------------------------------------------------------------------#
#----------------------------------- Private methods-----------------------------------------------#
#--------------------------------------------------------------------------------------------------#

    def __check_loaded_eeg(self):
        error=False
        try:
            error=len(self.eeg)<1
        except:
            error=True
        if(error):
            raise Exception('EEG not properly loaded.')

#--------------------------------------------------------------------------------------------------#

    def __cluster(self,artifact_markings:list)->list:
        if self.cluster_size>0:
            clustered_markings=[0]*self.n_samples
            last_detection=None
            for t in range(self.cluster_size+1,self.n_samples):
                if artifact_markings[t]==1:
                    clustered_markings[t]=1
                    if not 1 in artifact_markings[t-self.cluster_size:t]:
                        clustered_markings[t-1]=1
                        clustered_markings[t-2]=1
                    if last_detection!=None:
                        since_last_detection=t-last_detection
                        if since_last_detection<=self.cluster_size:
                            clustered_markings[last_detection:t]=[1]*since_last_detection
                    last_detection=t
            return clustered_markings
        else:
            return artifact_markings
            
#--------------------------------------------------------------------------------------------------#

    def __fast_cluster(self,last_detection:int,current_index:int,location_markings:list)->list:
        clustered_markings=location_markings
        if not 1 in location_markings[current_index-self.cluster_size:current_index]:
            clustered_markings[current_index-1]=1
            clustered_markings[current_index-2]=1
        if last_detection!=None:
            since_last_detection=current_index-last_detection
            if since_last_detection<=self.cluster_size:
                clustered_markings[last_detection:current_index]=[1]*since_last_detection
        return clustered_markings

#--------------------------------------------------------------------------------------------------#
#----------------------------------- Public methods------------------------------------------------#
#--------------------------------------------------------------------------------------------------#

    def load_eeg(self,eeg:list):
        """
        Loads a new EEG reading.
        """
        self.eeg = eeg
        self.n_samples=len(eeg)

#--------------------------------------------------------------------------------------------------#

    def set_cluster_size(self,cluster_size:int=0):
        self.cluster_size=cluster_size

#--------------------------------------------------------------------------------------------------#

    def peak_detection(self,window_size:int, sensitivity:int) -> list:
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
            artifact_locations[t]= 0 if abs(first_order_diferences[t])<sensitivity_multiplier*median_absolute_deviation[t] else 1
            
            # Cluster detections
            if(artifact_locations[t]==1):
                artifact_locations=self.__fast_cluster(last_detection,t,artifact_locations)
                last_detection=t
        return artifact_locations

#--------------------------------------------------------------------------------------------------#

    def threshold(self,threshold:float)->list:
        # Check if loaded eeg is of valid format
        self.__check_loaded_eeg()

        # Initialize artifact location markings
        artifact_locations=[0]*self.n_samples
        last_detection=None
        for t in range(self.n_samples):
            artifact_locations[t]= 0 if abs(self.eeg[t][0])<threshold else 1
            if(artifact_locations[t]==1):
                artifact_locations=self.__fast_cluster(last_detection,t,artifact_locations)
                last_detection=t
        return artifact_locations

#--------------------------------------------------------------------------------------------------#
