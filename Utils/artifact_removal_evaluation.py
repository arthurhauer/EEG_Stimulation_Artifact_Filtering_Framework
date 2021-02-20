
class ArtifactRemovalEvaluation:
    #--------------------------------------------------------------------------------------------------#
    #------------------------------------------- DOC---------------------------------------------------#
    #--------------------------------------------------------------------------------------------------#

    """
    Class developed for evaluating of stimulus artifact filtering methods in EEG signals.
    Version: 1.0.1
    Last modified by: Arthur Hauer
    Last modification date: 18/02/2021
    """

#--------------------------------------------------------------------------------------------------#
#----------------------------------------- Fields--------------------------------------------------#
#--------------------------------------------------------------------------------------------------#

    original = [[]]
    filtered = [[]]
    n_samples = 0


#--------------------------------------------------------------------------------------------------#
#-------------------------------------- Constructor------------------------------------------------#
#--------------------------------------------------------------------------------------------------#

    def __init__(self, original, filtered):
        self.original = original
        self.filtered = filtered

#--------------------------------------------------------------------------------------------------#
#----------------------------------- Private methods-----------------------------------------------#
#--------------------------------------------------------------------------------------------------#

    def __check_loaded_signals(self):
        error = False
        original_channels = len(self.original)
        filtered_channels = len(self.filtered)
        original_samples = len(self.original[0])
        filtered_samples = len(self.filtered[0])
        error = error or filtered_channels != filtered_channels
        error = error or original_samples != filtered_samples
        error = error or original_samples > 0
        for i in range(original_samples):
            error = error or len(self.original[i]) != len(self.filtered[i])
            if error:
                break
        if error:
            raise Exception('Signals not properly loaded.')
        n_samples = original_samples

#--------------------------------------------------------------------------------------------------#

    def __signal_to_noise_ratio_estimation(self, trial1, trial2):
        raise Exception("Not Implemented.")

#--------------------------------------------------------------------------------------------------#
#----------------------------------- Public methods------------------------------------------------#
#--------------------------------------------------------------------------------------------------#

    def artifact_reduction_ratio_estimation(self):
        raise Exception("Not Implemented.")
