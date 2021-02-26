from opensignalsreader import OpenSignalsReader
import matplotlib.pyplot as plt
from Utils.artifact_detection import *
from Utils.artifact_filtering import *
from tkinter.filedialog import askopenfilename
import tkinter as tk
import numpy as np

root=tk.Tk()
root.withdraw()

filename=askopenfilename()
data=np.genfromtxt(filename,usecols=(1,2,3,4,5,6,7),skip_header=4,delimiter=',',names=True)
readings=data[50:len(data)]

filtering = ArtifactFiltering(readings)
filtering.generate_stimulation_markings('peak_detection',cluster_size=10,window_size=25,sensitivity=0.02)
original_eeg=filtering.get_eeg()

artifact_locations=filtering.get_stimulation_markings()

filtered_eeg=filtering.blanking_interpolation()


plots=1
# plots=len(data[0])
for i in range(plots):
    plt.figure(i)
    plt.title=(original_eeg.dtype.names[i])
    plt.subplot(311)
    plt.plot(original_eeg[original_eeg.dtype.names[i]])


    plt.figure(i)
    plt.subplot(312)
    plt.plot(artifact_locations)


    plt.figure(i)
    plt.subplot(313)
    plt.plot(filtered_eeg[original_eeg.dtype.names[i]])

plt.show()