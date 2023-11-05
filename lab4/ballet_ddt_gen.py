import numpy as np
def calculatep():
    count = 0
    for i in range(16):
        for j in range(16):
            if (i+j)>=16 :
                count+=1
    p = count / 256
    return p

def ballet_ddt_gen():
    p = calculatep() # 有进位的概率
    ddt1=np.zeros([256,16]) # 无进位(1-p)^2
    ddt2=np.zeros([256,16]) # 一个进位2*p(1-p)
    ddt3=np.zeros([256,16]) # 都进位p^2
    for i in range(256):
        for j in range(256):
            x1=i%16
            x2=i//16
            x1_=j%16
            x2_=j//16
            din=i^j
            dout=((x1+x2)%16)^((x1_+x2_)%16)
            ddt1[din][dout]+=1
            dout = ((x1 + x2 + 1) % 16) ^ ((x1_ + x2_) % 16)
            ddt2[din][dout]+=1
            dout = ((x1 + x2 + 1) % 16) ^ ((x1_ + x2_+1) % 16)
            ddt3[din][dout]+=1

    ddt = ddt1*((1-p)**2)+ddt2*(2*p*(1-p))+ddt3*(p**2)
    ddt_int = np.around(ddt) # 四舍五入
    return ddt_int

if __name__ =='__main__':
    ddt_int=ballet_ddt_gen()
    for ele in ddt_int:
        print(ele)
