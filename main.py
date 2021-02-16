from opensignalsreader import OpenSignalsReader
import matplotlib.pyplot as plt
from Utils.artifact_detection import ArtifactDetection


acq = OpenSignalsReader('sample.txt')

readings=[[]]
readings[0]=acq.raw(1)

detection=ArtifactDetection(readings)
locations=detection.peak_detection(1000,0.1)

plt.figure(1)
plt.subplot(211)
plt.plot(acq.raw(1))

plt.figure(1)
plt.subplot(212)
plt.plot(locations)
plt.show()