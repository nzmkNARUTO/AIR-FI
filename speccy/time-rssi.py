import sys
from matplotlib import pyplot as plt
from spectrum_file import SpectrumFileReader
import pickle as cPickle
from scipy.signal import savgol_filter
from jiema import decode

def analysis(rssi_list,seprate):
    print("analysising")
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
    if rssi_list[i-1]>seprate:
        tempbins+=[[1,count]]
    else:
        tempbins+=[[0,count]]
    print(tempbins)
    tempbins=[i for i in tempbins if i[1]>500]
    for i in range(len(tempbins)-8):
        if tempbins[0][0]!=1 or tempbins[1][0]!=0 or tempbins[2][0]!=1 or tempbins[3][0]!=0 or\
            tempbins[4][0]!=1 or tempbins[5][0]!=0 or tempbins[6][0]!=1 or tempbins[7][0]!=0:
            tempbins.pop(0)
        else:
            break
    windows1=tempbins[0][1] + tempbins[2][1] + tempbins[4][1] + tempbins[6][1]
    windows0= tempbins[1][1] + tempbins[3][1] + tempbins[5][1]
    windows1/=4
    windows0/=3
    windows1=int(windows1)
    windows0=int(windows0)
    # if (windows1-windows0)/((windows0+windows1)/2)>0.15:
    #     windows0=windows1=(windows0+windows1)/2
    print(windows1,' ',windows0)
    bins=[]
    print(tempbins)
    for i in range(len(tempbins)):
        if tempbins[i][0]==0:
            times=tempbins[i][1]/(windows0*0.85)
        else:
            times=tempbins[i][1]/(windows1*0.85)
        if times>2:
            for j in range(int(times)):
                print(tempbins[i])
                bins+=[tempbins[i][0]]
        elif times<0.3:
            continue
        else:
            bins+=[tempbins[i][0]]
    bins=[str(x) for x in bins[:40]]
    bins=''.join(bins)
    print(bins)
    decode(bins)

def process(filename):
    rssi_list=[]
    
    f = open(filename, 'rb')
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
    y = savgol_filter(rssi_list, 10001,2)
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
    plt.savefig(str(filename).replace('bin','jpg'))
    analysis(tempbins,seprate)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print ("\nUsage: \n  $python analysis.py filename\n")
        exit(0)
    process(sys.argv[1])