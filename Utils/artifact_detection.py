import statistics
import Utils.utils as utils

class ArtifactDetection:
#--------------------------------------------------------------------------------------------------#
#------------------------------------------- DOC---------------------------------------------------#
#--------------------------------------------------------------------------------------------------#

    """
    Class developed for detetection of stimulus artifiact in EEG signals.
    Version: 1.0.0
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
        print('Init Artifact Detection Class')
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
        first_order_diferences=utils.first_order_differences(self.eeg)

        # Compute sliding windows median absolute deviation of first order differences
        median_absolute_deviation=utils.sliding_median_absolute_deviation(first_order_diferences,window_size)

        # Initialize sensitivity factor
        sensitivity_multiplier=1/sensitivity

        # Initialize artifact location markings
        artifact_locations=[0]*self.n_samples

        # Set artifact location marking to 1 if first order difference of sample is greater than a scaled median absolute deviation for the same sample
        for t in range(self.n_samples):
            artifact_locations[t]= 0 if abs(first_order_diferences[t])<sensitivity_multiplier*median_absolute_deviation[t] else 1

        return artifact_locations

#--------------------------------------------------------------------------------------------------#