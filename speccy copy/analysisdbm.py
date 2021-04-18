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
    plt.savefig("./dbm"+str(filename).replace("./data","").replace(".txt",".jpg"))

def analysing(filename1, filename2):
    t=1
    freqlist1={}
    freqlist2={}
    freqlist={}
    for i in range(2400,2500,t):
        freqlist1[i]=0
        freqlist2[i]=0
        freqlist[i]=0

    with open(filename1,"r") as off:
        lines1=off.readlines()
        off.close()
    print(len(lines1))

    with open(filename2,"r") as on:
        lines2=on.readlines()
        on.close()
    print(len(lines2))

    for line in tqdm(lines1[1:]):
        #print(line)
        if line[0]=='0':
            continue
        try:
            freq,dbm=str(line).split(' ')
            freq=int((int(eval(freq))-2400)/t)*t+2400
            dbm=int(eval(dbm))
            freqlist1[freq]+=dbm
        except:
            print(line)
            continue

    for line in tqdm(lines2[1:]):
        #print(line)
        if line[0]=='0':
            continue
        try:
            freq,dbm=str(line).split(' ')
            freq=int((int(eval(freq))-2400)/t)*t+2400
            dbm=int(eval(dbm))
            freqlist2[freq]+=dbm
        except:
            print(line)
            continue

    for i in tqdm(range(2400,2500,t)):
        freqlist[i]=freqlist2[i]-freqlist1[i]

    zero=[]
    for i in freqlist:
        if freqlist[i]==0:
            zero+=[i]
    for i in zero:
        freqlist.pop(i)

    print(freqlist)
    draw_from_dict(freqlist,len(freqlist),"/dbm.jpg")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print ("\nUsage: \n  $python analysis.py filename\n")
        exit(0)
    analysing(sys.argv[1],sys.argv[2])