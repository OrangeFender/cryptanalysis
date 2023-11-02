import numpy as np
import json

def calculatep():
    count = 0
    for i in range(256):
        for j in range(256):
            if (i+j)>=256 :
                count+=1
    p = count / (2**16)
    return p

#A(x||y)->x+y
#x和y均为8bit，故输入为16bit。
#x+y为输出，8bit
def ballet_ddt_gen():
    p = calculatep() # 有进位的概率
    ddt1=np.zeros([2**16,2**8]) # 无进位(1-p)^2
    ddt2=np.zeros([2**16,2**8]) # x进位2*p(1-p)
    ddt3=np.zeros([2**16,2**8]) # y进位2*p(1-p)
    ddt4=np.zeros([2**16,2**8]) # 都进位p^2
    #第一个输入x||y
    for i in range(65536):
        print(i)
        #第二个输入x'||y'
        for j in range(65536):
            y=i&0x00ff
            x=(i&0xff00)>>8
            y_=j&0x00ff
            x_=(j&0xff00)>>8

            din=i^j
            dout=((x+y)&0xff)^((x_+y_)&0xff)
            ddt1[din][dout]+=1

            dout = ((x + y + 1)&0xff) ^ ((x_ + y_)&0xff)
            ddt2[din][dout]+=1

            dout = ((x + y )&0xff) ^ ((x_ + y_ + 1)&0xff)
            ddt3[din][dout]+=1

            dout = ((x + y +1 )&0xff) ^ ((x_ + y_+1)&0xff)
            ddt4[din][dout]+=1

    ddt = ddt1*((1-p)**2)+ddt2*(2*p*(1-p))+ddt3*(p**2)
    ddt_int = np.around(ddt) # 四舍五入
    return ddt_int

if __name__ =='__main__':
    ddt_int=ballet_ddt_gen()

    with open('dtt_8.json','w') as file:
        json.dump(ddt_int, file)
