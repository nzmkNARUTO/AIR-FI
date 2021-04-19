from matplotlib import pyplot as plt
import sys
from tqdm import tqdm
from spectrum_file import SpectrumFileReader
import pickle as cPickle
import sys

def process(fn):
    rssi_list=[]
    print ("processing '%s':" % fn)
    f = open(fn, 'rb')
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
    print(len(rssi_list))
    flag=False
    # process_bar=tqdm(total=len(rssi_list))
    start=0
    while start<(len(rssi_list)/2):#控制起始位置
        # process_bar.update(1)
        windows=100
        while windows<(len(rssi_list)/2):#控制窗口长度
            bins=[]
            now=start
            avg_last=[]
            seprate=8
            while now<(len(rssi_list)-windows):#控制当前位置
                avg=sum(rssi_list[now:now+windows])/windows
                if avg>seprate:
                    bins+=[1]
                else:
                    bins+=[0]
                avg_last+=[avg]
                print('windows:',windows,' start:',start,' now:',now,' avg:',avg,' seprate',seprate,' bins',bins)
                if len(bins)==8:
                    if bins[0]!=1 or bins[1]!=0 or bins[2]!=1 or bins[3]!=0 or\
                        bins[4]!=1 or bins[5]!=0 or bins[6]!=1 or bins[7]!=0:
                        bins.pop(0)
                        avg_last.pop(0)
                    else:
                        flag=True
                        seprate=sum(avg_last)/len(avg_last)
                now+=windows
            if flag:
                break
            windows+=100
        if flag:
            break
        start+=100
        # print(windows)
    print(bins)
    # process_bar.close()

    plt.bar(range(len(rssi_list)),rssi_list)
    plt.savefig("./test.jpg")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print ("\nUsage: \n  $python analysis.py filename\n")
        exit(0)
    process(sys.argv[1])