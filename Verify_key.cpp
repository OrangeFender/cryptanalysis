#include "include.h"
#include <string>
#include <iostream>
#include <fstream>

void encrypt(Key_Stecker* ks_all, std::string plain, int length, std::ofstream * output){
    //初始化各种参数
    std::string cipher="";
    int *stecker=ks_all->stecker;
    int mid_key=ks_all->mid_key;
    int quick_key=ks_all->quick_key;
    //开始加密
    for(int i=0;i<length;i++){
        

        int input=plain[i]-'a';
        int tmp=0;

        tmp=stecker[input];
        
        tmp=rotors_and_reflector(tmp,mid_key,quick_key);

        tmp=stecker[tmp];
        
        cipher=cipher+char(tmp+'a');

        // change *_key
        if (quick_key == 0)
        {
        mid_key = (mid_key + 25) % 26;
        }
        quick_key = (quick_key + 25) % 26;
    }
    *output<<cipher<<std::endl;
}