import math
from Utils.utils import Utils

class ArtifactRemovalEvaluation:
    #--------------------------------------------------------------------------------------------------#
    #------------------------------------------- DOC---------------------------------------------------#
    #--------------------------------------------------------------------------------------------------#

    """
    Class developed for evaluating of stimulus artifact filtering methods in EEG signals.
    Version: 1.1.0
    Last modified by: Arthur Hauer
    Last modification date: 25/03/2021
    """

#--------------------------------------------------------------------------------------------------#
#----------------------------------------- Fields--------------------------------------------------#
#--------------------------------------------------------------------------------------------------#

    original = [[]]
    filtered = [[]]
    clean = [[]]
    n_samples = 0


#--------------------------------------------------------------------------------------------------#
#-------------------------------------- Constructor------------------------------------------------#
#--------------------------------------------------------------------------------------------------#


    def __init__(self, original, filtered, clean):
        self.original = original
        self.filtered = filtered
        self.clean = clean

#--------------------------------------------------------------------------------------------------#
#----------------------------------- Private methods-----------------------------------------------#
#--------------------------------------------------------------------------------------------------#

    def __check_loaded_signals(self):
        error = False
        original_channels = len(self.original)
        filtered_channels = len(self.filtered)
        clean_channels = len(self.clean)
        original_samples = len(self.original[0])
        filtered_samples = len(self.filtered[0])
        clean_samples = len(self.clean[0])
        error = error or original_channels != filtered_channels
        error = error or original_channels != clean_channels
        error = error or original_channels < 1
        error = error or original_samples != filtered_samples
        error = error or original_samples != clean_samples
        error = error or original_samples < 1
        for i in range(original_samples):
            error = error or len(self.original[i]) != len(self.filtered[i])
            error = error or len(self.original[i]) != len(self.clean[i])
            if error:
                break
        if error:
            raise Exception('Signals not properly loaded.')
        n_samples = original_samples




#--------------------------------------------------------------------------------------------------#
#----------------------------------- Public methods------------------------------------------------#
#--------------------------------------------------------------------------------------------------#

    def artifact_reduction_ratio_estimation(self,method:str='clean_reference',**kwargs):
        raise Exception("Not Implemented.")

#--------------------------------------------------------------------------------------------------#

    def signal_to_noise_ratio_estimation(self,method:str='clean_reference',**kwargs)->list:
        if method=='clean_reference': 
            raise Exception("Not Implemented.")

#--------------------------------------------------------------------------------------------------#
#---------------------------------- Private methods------------------------------------------------#
#--------------------------------------------------------------------------------------------------#

    def _clean_reference_snr_estimation(self,poluted:list,clean:list)->list:
        """
        Method based on the eeg blanking algorithm described on
        { X. An, G. Stylios,
         “Comparison of motion artefact reduction methods and the implementation of adaptive motion artefact reduction in wearable electrocardiogram monitoring”,
         10.3390/s20051468 }.
        This method assumes the hidden EEG behind stimulations has amplitude similar any non-estimulated EEG acquisitions on the same channel
        """
        # Check if loaded signals have valid format
        self.__check_loaded_signals()
        snr=[]
        for channel_index in range(len(original)):
            sn=clean[channel_index]
            snL=poluted[channel_index]
            sn2=Utils.power_list(sn)
            sn_snL=Utils.subtract_lists(snL,sn)
            sn_snL2=Utils.power_list(sn_snL)
            Esn2=Utils.sum_list(sn2)
            Esn_snL2=Utils.sum_list(sn_snL2)
            snr[channel_index]=10*math.log(Esn2/Esn_snL2)
        return snr
#--------------------------------------------------------------------------------------------------#
