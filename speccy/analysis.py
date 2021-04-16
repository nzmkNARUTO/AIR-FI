from matplotlib import pyplot as plt
import sys
from tqdm import tqdm
def draw_from_dict(dicdata,RANGE, filename):
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
    plt.savefig("./show"+str(filename).replace("./data","").replace(".txt",".jpg"))

def analysing(filename):
    t=1
    freqlist={}
    freqcount={}
    for i in range(2400,2500,t):
        freqlist[i]=0
        freqcount[i]=0

    with open(filename,"r") as off:
        lines=off.readlines()
        off.close()
    print(len(lines))

    for line in tqdm(lines[1:]):
        #print(line)
        if line[0]=='0':
            continue
        freq,dbm=str(line).split(' ')
        freq=int((int(eval(freq))-2400)/t)*t+2400
        dbm=int(eval(dbm))
        freqlist[freq]+=dbm
        freqcount[freq]+=1

    zero=[]
    for i in tqdm(freqlist):
        try:
            freqlist[i]/=freqcount[i]
        except:
            pass
        if freqlist[i]==0:
            zero+=[i]
    for i in tqdm(zero):
        freqlist.pop(i)
    mindbm=min(freqlist.values())
    for i in tqdm(freqlist):
        freqlist[i]-=-120
    print(freqlist)
    draw_from_dict(freqlist,len(freqlist),filename)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print ("\nUsage: \n  $python analysis.py filename\n")
        exit(0)
    analysing(sys.argv[1])