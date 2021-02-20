from opensignalsreader import OpenSignalsReader
import matplotlib.pyplot as plt
from Utils.artifact_detection import *
from Utils.artifact_filtering import *
from tkinter.filedialog import askopenfilename
import numpy as np

filename=askopenfilename()
# usecols=(1,2,3,4,6)
data=np.genfromtxt(filename,skip_header=4,delimiter=',',names=True)
# data=np.genfromtxt(filename,delimiter=',',names=["x","y"])
readings=data[50:len(data)]


# readings=[[]]
# readings[0]=acq.raw(1)

filtering = ArtifactFiltering(readings)
filtering.generate_stimulation_markings('peak_detection',cluster_size=10,window_size=10,sensitivity=0.01)
original_eeg=filtering.get_eeg()

artifact_locations=filtering.get_stimulation_markings()

filtered_eeg=filtering.blanking_interpolation()


# plots=1
plots=len(data[0])
for i in range(plots):
    plt.figure(i)
    plt.plot(data[data.dtype.names[i]])
    # plt.figure(i)
    # plt.title=(original_eeg.dtype.names[i])
    # plt.subplot(311)
    # plt.plot(original_eeg[original_eeg.dtype.names[i]])


    # plt.figure(i)
    # plt.subplot(312)
    # plt.plot(artifact_locations)


    # plt.figure(i)
    # plt.subplot(313)
    # plt.plot(filtered_eeg[original_eeg.dtype.names[i]])

plt.show()