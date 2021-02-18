from opensignalsreader import OpenSignalsReader
import matplotlib.pyplot as plt
from Utils.artifact_detection import *

acq = OpenSignalsReader('sample.txt')

readings=[[]]
readings[0]=acq.raw(1)
plt.figure(1)
plt.subplot(211)
plt.plot(readings[0])

detection=ArtifactDetection(readings,200)

locations_peak=detection.peak_detection(25,3)
plt.figure(1)
plt.subplot(212)
plt.plot(locations_peak)

plt.show()