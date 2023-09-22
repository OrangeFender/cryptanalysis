#!/usr/bin/python3
S = [2, 1, 0, 4, 3, 5, 7, 6, 8, 9, 24, 11, 20, 13, 14, 15, 16, 17,18, 19, 12, 21, 22, 23, 10, 25]
QUICK = [0, 18, 24, 10, 12, 20, 8, 6, 14, 2, 11, 15, 22, 3, 25, 7, 17, 13, 1, 5, 23, 9, 16, 21, 19, 4]
MID = [0, 10, 4, 2, 8, 1, 18, 20, 22, 19, 13, 6, 17, 5, 9, 3, 24, 14, 12, 25, 21, 11, 7, 16, 15, 23]
T = [10, 20, 14, 8, 25, 15, 16, 21, 3, 18, 0, 23, 13, 12, 2, 5, 6, 19, 9, 17, 1, 7, 24, 11, 22, 4]

rQUICK, rMID = list(QUICK), list(MID)
for i in range(26):
    rQUICK[QUICK[i]] = rMID[MID[i]] = i

q = [0,18,9,13,25,19,7,15,6,21,3,10,4,16,8,11,22,17,1,24,5,23,12,20,2,14]
m = [0,5,3,14,2,13,11,22,4,15,1,21,18,10,17,24,23,12,6,9,7,20,8,25,16,19]
s = [7,17,25,16,19,21,9,2,12,10,3,22,4,23,8,11,24,15,18,5,14,20,1,6,0,13]

in_ = list("wetter")
I = [ord(item) - 97 for item in in_]

# 两个环路crib s1，s2
s1 = I[0:2]+[I[3]]
s2 = I[1:3]+[I[5]]

rq,rm,rs = list(q),list(m),list(s)

for i in range(26):
    rq[q[i]] = rm[m[i]] = rs[s[i]] = i

def R(rq,rm,rs,x,y,z):
    def func(L):
        L = (L+x)%26
        temp = (rq[L]-x)%26
        temp = (temp+y)%26
        temp2 = (rm[temp]-y)%26
        temp2 = (temp2+z)%26
        temp3 = (rs[temp2]-z)%26

        return temp3
    return func

# general Rotors
def Rg(rotors = [], setoffs = []):
    """通用的扰频器，rotors是转子列表，setoffs是对应偏移量列表
    返回一个函数，返回的函数接受一个参数并返回扰频器的输出值
    """
    def func(L):
        for rotor, setoff in zip(rotors, setoffs):
            L = (rotor[(L + setoff) % 26] - setoff) % 26
        return L
    return func


def machine(R,T,R_re):
    """除去接线板之后的engima机器，R，T，R_re分别是正向扰频器，反射板，逆向扰频器
    返回一个函数，返回的函数接受一个参数并输出machine机的返回值
    """
    def func(L):
        return R_re(T[R(L)])
    return func

# 程序中所有的除去接线板的enigma机器简称为machine

def enigma(link,machine):
    def func(L):
        return link[machine(link[L])]
    return func


def find_circuit(machines=[]):
    """寻找环路crib，machines是machine状态机的列表
    返回一个列表，列表中包含子列表，每个子列表代表一个环路crib
    """
    circuits = []
    for i in range(26):
        L = [i]
        temp = i
        for machine in machines:
            temp = machine(temp)
            L.append(temp)
        if i == L.pop():
            circuits.append(list(L))
        L.clear()
    return circuits


def conflict(links = []):
    """检测冲突，links代表一种候选解中的所有连线状态
    links列表中包含许多set，每个set中两个值代表连线
    返回一个bool值，若检测到冲突返回True，没有冲突则返回False
    """

    for i in links:
        for j in links:
            if len(i&j) == 1:
                return True
    return False

def all_machine():
    """machine生成器，调用此函数生成所有可能状态的machine机器
    返回一个二维列表，两个偏移量x,y分别作为第一维第二维的索引值即可检索到对应的machine机器
    (返回一个函数的二位列表）
    """
    machine_all = []
    for i in range(26):
        machines_ = []
        for j in range(26):
            Q = Rg([rQUICK,rMID],[i,j])
            M = Rg([MID,QUICK],[j,i])
            machinei = machine(Q,T,M) 
            machines_.append(machinei)
        machine_all.append(machines_)
    return machine_all

# attack函数和check函数都要对d进行枚举，d代表中速转子转动的情况

def attack(d):
    """攻击函数，实现攻击算法
    
    """
    machines = all_machine()
    K1,K2=[],[]
    res = []
    for x in range(26):
        for y in range(26):
            machines1 = [machines[x][y-1 if d<=0 else y],machines[(x-1)%26][y-1 if d<=1 else y],machines[(x-3)%26][y-1 if d<=3 else y]]
            machines2 = [machines[(x-1)%26][y-1 if d<=1 else y],machines[(x-2)%26][y-1 if d<=2 else y],machines[(x-5)%26][y-1 if d<=5 else y]]
            circuits1 = find_circuit(machines1)
            circuits2 = find_circuit(machines2)
            for circuit1 in circuits1:
                for circuit2 in circuits2:
                    temp = [set([a,b]) for a,b in zip(s1,circuit1)]
                    temp += [set([a,b]) for a,b in zip(s2,circuit2)]
                    if not conflict(temp):
                        temp_machine = machines[(x-4)%26][y-1 if d<=4 else y]
                        link_p = temp_machine(circuit1[1])
                        temp.append(set([15,link_p]))
                        if not conflict(temp):
                            res.append(temp)
                            K1.append([x,y])

    # 将res中的连线转换为列表形式K2
    for i in range(len(res)):
        ttt = [j for j in range(26)]
        for item in res[i]:
            k,v=item
            ttt[k],ttt[v]=v,k
        K2.append(ttt)
    return K1,K2


def check(d):
    k1,k2=attack(d)
    machines = all_machine()
    for i in range(len(k1)):
        x,y = k1[i]
        en = [enigma(k2[i],machines[l][y]) for l in range(x,x-d,-1)]
        en += [enigma(k2[i],machines[l][y-1]) for l in range(x-d,x-6,-1)]
        checkit=''
        for j in range(len(I)):
            checkit+=chr(en[j](I[j])+97)
        print(checkit)

        
        
def task1():
    machines = all_machine()
    x,y=4,4
    link=[2, 1, 0, 4, 3, 5, 7, 6, 8, 9, 24, 11, 20, 13, 14, 15, 16, 17,18, 19, 12, 21, 22, 23, 10, 25]
    en = [enigma(link,machines[l%26][y]) for l in range(x,x-6,-1)]
    # en.append(enigma(link,machines[x-6][y-1]))
    checkit=''
    for j in range(6):
        checkit+=chr(en[j](I[j])+97)
    return checkit

def all_attack():
    k1,k2=[],[]
    for d in range(7):
        a,b = attack(d)
        k1 += a
        k2 += b
    return k1,k2

def all_check():
    k1,k2=all_attack()
    for d in range(7):
        check(d)


if __name__ == "__main__":
    print("枚举中速转子转动的位置有七种情况，分别是不发生转动和在wetter中的任一位置开始发生转动")
    k1,k2=all_attack()
    print("共获得{}个解:".format(len(k1)))
    for K1,K2 in zip(k1,k2):
        print(f"{K1}  {K2}")


