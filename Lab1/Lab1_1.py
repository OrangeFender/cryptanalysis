def Enigma(s): #输入明文字符串，输出加密后的列表
    K2=(4,4)
    S = [2, 1, 0, 4, 3, 5, 7, 6, 8, 9, 24, 11, 20, 13, 14, 15, 16, 17,18, 19, 12, 21, 22, 23, 10, 25]
    QUICK = [0, 18, 24, 10, 12, 20, 8, 6, 14, 2, 11, 15, 22, 3, 25, 7, 17, 13, 1, 5, 23, 9, 16, 21, 19, 4]
    quick_map = {value: index for index, value in enumerate(QUICK)}
    MID = [0, 10, 4, 2, 8, 1, 18, 20, 22, 19, 13, 6, 17, 5, 9, 3, 24, 14, 12, 25, 21, 11, 7, 16, 15, 23]
    mid_map = {value: index for index, value in enumerate(MID)}
    T = [10, 20, 14, 8, 25, 15, 16, 21, 3, 18, 0, 23, 13, 12, 2, 5, 6, 19, 9, 17, 1, 7, 24, 11, 22, 4]
    #接线板字符转换
    s = list(s)
    for i in range(len(s)):
        s[i]= chr(S[ord(s[i])-97]+97)
    # print(s)

    #扰频器组合（2转子）
    pos_quick = K2[0] #转子转动变量，模26
    pos_mid = K2[1]
    for i in range(len(s)):
        s[i] = chr(QUICK[(ord(s[i])-97-pos_quick+26)%26]+97)
        s[i] = chr(MID[(ord(s[i])-97-pos_mid+26)%26]+97)
        pos_quick = (pos_quick+25)%26
        if(pos_quick == K2[0]):
            pos_mid = (pos_mid+25)%26
    # print(s)

    #反射器
    s[i]= chr(T[ord(s[i])-97]+97)
    QUICK.reverse()
    MID.reverse()
    # print(QUICK)

    #扰频器组合（2转子）
    for i in range(len(s)):
        s[i] = chr(mid_map[(ord(s[i])-97+pos_mid)%26]+97)
        s[i] = chr(quick_map[(ord(s[i])-97+pos_quick)%26]+97)
        pos_quick = (pos_quick+25)%26
        if(pos_quick == K2[0]):
            pos_mid = (pos_mid+25)%26
    # print(s)

    #接线板字符转换
    s[i]= chr(S[ord(s[i])-97]+97)
    return s

if __name__ == '__main__':
    s="wetter"
    print(s)
    a = Enigma(s)
    print(a)
        
