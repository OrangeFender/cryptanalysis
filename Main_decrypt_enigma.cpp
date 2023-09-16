#include "include.h"
#include <iostream>
#include <fstream>

int main(){
    std::ofstream output_key0;
    output_key0.open("key_step0.txt");
    if(!output_key0.is_open()){
        std::cerr<<"无法打开文件"<<std::endl;
        return 1;
    }
    std::ofstream output_key1;
    output_key1.open("key_step1.txt");
    if(!output_key1.is_open()){
        std::cerr<<"无法打开文件"<<std::endl;
        return 1;
    }
    //step0，即通过环路获得的原始密钥
    int characteristc_array[4]={1,1,0,1};
    bool **key=find_possible_key(4, characteristc_array);
    for(int i=25;i>-1;i--){
        for(int j=25;j>-1;j--){
            if(key[i][j]==1){
                output_key0<<i<<" "<<j<<std::endl;
            }
        }
    }
    //step1，经过相邻环路的筛选，同时构造出完整key的结构
    std::list<Key_Stecker*>* key_stecker_list=step1_select_valid_key(key);
    for(Key_Stecker* sk:*key_stecker_list){
        output_key1<<sk->key[0]<<" "<<sk->key[1]<<std::endl;
    }
}