#include <iostream>

class Enigma{
    const char S[26]={2, 1, 0, 4, 3, 5, 7, 6, 8, 9, 24, 11, 20, 13, 14, 15, 16, 17,18, 19, 12, 21, 22, 23, 10, 25};
    const char QUICK[26]={0, 18, 24, 10, 12, 20, 8, 6, 14, 2, 11, 15, 22, 3, 25, 7, 17, 13, 1, 5, 23, 9, 16, 21, 19, 4};
    const char QUICKrev[26]={0, 18, 9, 13, 25, 19, 7, 15, 6, 21, 3, 10, 4, 17, 8, 11, 22, 16, 1, 24, 5, 23, 12, 20, 2, 14};
    const char MID[26]={0, 10, 4, 2, 8, 1, 18, 20, 22, 19, 13, 6, 17, 5, 9, 3, 24, 14, 12, 25, 21, 11, 7, 16, 15, 23};
    const char MIDrev[26]={0, 5, 3, 15, 2, 13, 11, 22, 4, 14, 1, 21, 18, 10, 17, 24, 23, 12, 6, 9, 7, 20, 8, 25, 16, 19};
    const char T[26]={10, 20, 14, 8, 25, 15, 16, 21, 3, 18, 0, 23, 13, 12, 2, 5, 6, 19, 9, 17, 1, 7, 24, 11, 22, 4};
    int QUICK_bias=0;
    int MID_bias=1;
    char ENC(char m);
};
char Enigma::ENC(char m){
    if(m>=26){
        std::cout<<"m should be number less than 26"<<std::endl;
    }
    if(QUICK_bias==0)
        MID_bias--;
    char tmp=S[m];
    tmp=QUICK[(tmp+QUICK_bias)%26];
    tmp=MID[(tmp+MID_bias)%26];
    tmp=T[tmp];
    tmp=MIDrev[tmp];
    tmp=QUICKrev[tmp];
    QUICK_bias--%26;
    return tmp;
}