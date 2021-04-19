from matplotlib import pyplot as plt
from spectrum_file import SpectrumFileReader
import pickle as cPickle
from scipy.signal import savgol_filter

rssi_list=[]
f = open("./spectral_data/0.1.bin", 'rb')
while True:
    try:
        device_id, ts, sample_data = cPickle.load(f)
        for tsf, freq, noise, rssi, pwrs in SpectrumFileReader.decode(sample_data):
            rssi_list+=[rssi]
            # print (device_id, ts, tsf, freq, noise, rssi)
            # for carrier_freq, pwr_level in pwrs.items():
            #     print (carrier_freq, pwr_level)
    except EOFError:
        break
f.close()
print(len(rssi_list))
y = savgol_filter(rssi_list, 801, 3)
x=range(len(y))
print(len(y))
plt.plot(x,rssi_list)
plt.plot(x,y, color='red')
plt.savefig("./test.jpg")