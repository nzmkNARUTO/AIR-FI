from matplotlib import pyplot as plt
import sys
from tqdm import tqdm
from spectrum_file import SpectrumFileReader
import pickle as cPickle
import sys
import numpy as np

def process(fn):
    rssi_list=[]
    print ("processing '%s':" % fn)
    f = open(fn, 'rb')
    while True:
        try:
            device_id, ts, sample_data = cPickle.load(f)
            for tsf, freq, noise, rssi, pwrs in SpectrumFileReader.decode(sample_data):
                rssi_list+=[[ts,rssi]]
                # print (device_id, ts, tsf, freq, noise, rssi)
                # for carrier_freq, pwr_level in pwrs.items():
                #     print (carrier_freq, pwr_level)
        except EOFError:
            break
    analysis(rssi_list,fn)

def draw_from_dict(dicdata,RANGE,filename):
    print("\ndrawing")
    #dicdata：字典的数据。
    #RANGE：截取显示的字典的长度。
    #heng=0，代表条状图的柱子是竖直向上的。heng=1，代表柱子是横向的。考虑到文字是从左到右的，让柱子横向排列更容易观察坐标轴。
    by_value = sorted(dicdata.items(),key = lambda item:item[1],reverse=True)
    x = []
    y = []
    for d in by_value:
        x.append(d[0])
        y.append(d[1])

    plt.bar(x[0:RANGE], y[0:RANGE])
    plt.savefig("./"+str(filename).replace(".bin",".jpg"))

def analysis(rssi_list,filename):
    print("analysising")
    rssi={}
    print(len(rssi_list))
    lasttime=0
    count=1
    i=0
    for line in tqdm(rssi_list):
        if lasttime==line[0]:
            try:
                rssi[i]+=eval(str(line[1]))
            except:
                rssi[i]=eval(str(line[1]))
            count+=1
            lasttime=line[0]
        else:
            try:
                rssi[i]/=count
            except:
                rssi[i]=0
            count=1
            lasttime=line[0]
            i+=1
    rssi.pop(len(rssi)-1)
    draw_from_dict(rssi,len(rssi),filename)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print ("\nUsage: \n  $python analysis.py filename\n")
        exit(0)
    process(sys.argv[1])