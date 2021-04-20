from os import sep
from matplotlib import pyplot as plt
from spectrum_file import SpectrumFileReader
import pickle as cPickle
from scipy.signal import savgol_filter

def analysis(rssi_list,seprate):
    print("analysising")
    print(len(rssi_list))
    tempbins=[]
    count=0
    for i in range(len(rssi_list)-1):
        if rssi_list[i]==rssi_list[i+1]:
            count+=1
        else:
            if rssi_list[i]>seprate:
                tempbins+=[[1,count]]
            else:
                tempbins+=[[0,count]]
            count=0
    for i in range(len(tempbins)-8):
        if tempbins[0][0]!=1 or tempbins[1][0]!=0 or tempbins[2][0]!=1 or tempbins[3][0]!=0 or\
            tempbins[4][0]!=1 or tempbins[5][0]!=0 or tempbins[6][0]!=1 or tempbins[7][0]!=0:
            tempbins.pop(0)
            break
    windows=tempbins[0][1] + tempbins[1][1] + tempbins[2][1] + tempbins[3][1] +\
            tempbins[4][1] + tempbins[5][1] + tempbins[6][1] + tempbins[7][1]
    windows/=8
    windows=int(windows)
    bins=[]
    for i in range(len(tempbins)):
        times=tempbins[i][1]/windows
        if times>1.5:
            for i in range(int(times)):
                bins+=[tempbins[i][0]]
        else:
            bins+=[tempbins[i][0]]
    print(bins)

rssi_list=[]
f = open("./spectral_data/0.5.3.bin", 'rb')
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
y = savgol_filter(rssi_list, 1801, 2)
x=range(len(y))
tempbins=[]
max_y=max(y)
min_y=min(y)
seprate=(max_y+min_y)/2
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