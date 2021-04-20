from os import sep
from matplotlib import pyplot as plt
from spectrum_file import SpectrumFileReader
import pickle as cPickle
from scipy.signal import savgol_filter

def analysis(rssi_list,seprate):
    print("analysising")
    tempbins=[]
    bins=[]
    for i in range(len(rssi_list)):
        if rssi_list[i]>seprate:
            tempbins+=[1]
        else:
            tempbins+=[0]
    print(tempbins)
    while tempbins[0]==0:
        tempbins.pop(0)
    for i in range(len(tempbins)-1):
        if tempbins[i]>tempbins[i+1]:
            bins+=[1]
        if tempbins[i]<tempbins[i+1]:
            bins+=[0]
    for i in range(len(bins)-8):
        if bins[0]!=1 or bins[1]!=0 or bins[2]!=1 or bins[3]!=0 or\
            bins[4]!=1 or bins[5]!=0 or bins[6]!=1 or bins[7]!=0:
            bins.pop(0)
        else:
            break
    print(bins)

rssi_list=[]
f = open("./spectral_data/neu!1.bin", 'rb')
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
y = savgol_filter(rssi_list, 201,3)
x=range(len(y))
tempbins=[]
max_y=max(y)
min_y=min(y)
seprate=(max_y+min_y)/2
print(seprate)
# seprate=5
for i in range(len(y)):
    if y[i]>seprate:
        tempbins+=[max_y]
    else:
        tempbins+=[min_y]
plt.plot(x,rssi_list)
plt.plot(x,y, color='green')
plt.plot(x,tempbins,color='red')
plt.savefig("./test.jpg")
analysis(tempbins,seprate)