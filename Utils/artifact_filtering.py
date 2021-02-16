from Utils.artifact_detection import ArtifactDetection

class ArtifactFiltering:
#--------------------------------------------------------------------------------------------------#
#------------------------------------------- DOC---------------------------------------------------#
#--------------------------------------------------------------------------------------------------#

    """
    Class developed for filtering of stimulus artifiact in EEG signals.
    Version: 1.0.0
    Authored by: Arthur Hauer
    Last modified: 16/02/2021
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
        self.stimulation_markings

    def __check_loaded_eeg(self):
        error=False
        try:
            error=len(self.eeg[0])<1
        except:
            error=True
        if(error):
            raise Exception('EEG not properly loaded.')

    def __blank_signal(self)->list:
        print('hey!')

    def load_eeg(self, eeg:list):
        self.eeg=eeg
        self.n_samples=len(eeg[0])

    def load_stimulation_markings(self,stimulation_markings:list):
        self.stimulation_markings=stimulation_markings

    def generate_stimulation_markings(self,method:str='peak_detection',**kwargs):
        detection=ArtifactDetection(self.eeg)
        if method=='peak_detection':
            self.stimulation_markings=detection.peak_detection(kwargs.get('window_size'),kwargs.get('sensitivity'))
        elif method=='threshold':
            self.stimulation_markings=detection.threshold(kwargs.get('threshold'),kwargs.get('smoothing'))
        else:
            raise Exception("Detection method invalid!")

    def template_subtraction(self):
        print('template_subtraction!')

    def reference_signal_subtraction(self):
        print('reference_signal_subtraction!')

    def blanking_interpolation(self):
        print('blanking_interpolation!')

    def blanking_gaussian_distribution(self):
        print('blanking_gaussian_distribution!')

    def common_average_reference(self):
        print('common_average_reference!')

    def linear_regression_reference(self):
        print('linear_regression_reference!')

    def sys_id_wiener_filtering(self):
        print('sys_id_wiener_filtering!')