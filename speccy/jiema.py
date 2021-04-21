def xor(a,b):
    c = ''
    minlen = min(len(a),len(b))
    for i in range(minlen):
        if(a[len(a)-i-1]==b[len(b)-i-1]):
            d = '0'
        else:
            d='1'
        c = d+c
    if(len(a)>minlen):
        c = a[:len(a)-minlen]+c
    if(len(b)>minlen):
        c = b[:len(b)-minlen]+c
    return c


def decode(data):
    if(len(data)!=40):
        print("数据包长度不符")
    else:
        head = data[0:8]
        h = "10101010"
        if(head != h):
            print("包头不符")
        else:
            data1 = data[8:-8]
            stri = ""
            for i in range(0,3):
                di = data1[8*i : 8*(i+1)]
                print(di,end=' ')
                si = int(di, 2)
                print(chr(si))
                stri += chr(si)
            print(stri)

            data2 = data[:-8]

            crc = '0'
            g = '00110001'
            for i in range(0,4):
                crc = xor(crc,data2[8*i:8*(i+1)])
                for j in range(0,8):
                    if (crc[0] == '1'):
                        crc = xor((crc[1:]+'0'), g)
                    else:
                        crc = crc[1:]+'0'
            if(crc==data[-8:]):
                print("校验正确")
            else:
                print("校验错误")

