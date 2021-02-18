from opensignalsreader import OpenSignalsReader
import matplotlib.pyplot as plt
from Utils.artifact_detection import *
from Utils.artifact_filtering import *

acq = OpenSignalsReader('sample.txt')

readings=[[]]
readings[0]=acq.raw(1)

filtering = ArtifactFiltering(readings)
filtering.generate_stimulation_markings('peak_detection',cluster_size=100,window_size=25,sensitivity=3)
original_eeg=filtering.get_eeg()[0]

plt.figure(1)
plt.subplot(311)
plt.plot(original_eeg)

artifact_locations=filtering.get_stimulation_markings()

plt.figure(1)
plt.subplot(312)
plt.plot(artifact_locations)

filtered_eeg=filtering.blanking_interpolation()[0]

plt.figure(1)
plt.subplot(313)
plt.plot(filtered_eeg)

plt.show()