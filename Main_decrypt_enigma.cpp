#include "include.h"
#include <iostream>
#include <fstream>
#include <string>

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
    std::ofstream output_key2;
    output_key2.open("key_step2.txt");
    if(!output_key1.is_open()){
        std::cerr<<"无法打开文件"<<std::endl;
        return 1;
    }


    //step0，即通过环路获得的原始密钥
    int characteristic_array[6]={1,1,0,1,0,0};
    bool **key=find_possible_key(6, characteristic_array);
    //打印step0获得的密钥
    for(int i=25;i>-1;i--){
        for(int j=25;j>-1;j--){
            if(key[i][j]==1){
                output_key0<<i<<" "<<j<<std::endl;
            }
        }
    }


    //step1，经过相邻环路的筛选，同时构造出完整key的结构
    std::list<Key_Stecker*>* key_stecker_list_pre=step1_select_valid_key(key);
    //打印step1获得的密钥
    for(Key_Stecker* ks:*key_stecker_list_pre){
        output_key1<<ks->mid_key<<" "<<ks->quick_key<<std::endl;
    }


    //step2+3，恢复接线板，其中step2是利用crib中的环路恢复，step3是利用crib中的非环路恢复
    std::string plain="wetter";
    std::list<Key_Stecker *> * key_stecker_list=step2_delete_invalid_key(key_stecker_list_pre, plain.length(), characteristic_array, plain);
    //打印step2+3获得的密钥，此时已经获得满足crib的密钥
    output_key2<<"明文: "<<plain<<std::endl;
    output_key2<<"共获得密钥个数: "<<key_stecker_list->size()<<std::endl;
    output_key2<<"(mid_key, quick_key), stecker_key"<<std::endl;
    for(Key_Stecker* ks_all:*key_stecker_list){  
        output_key2<<"("<<ks_all->mid_key<<", "<<ks_all->quick_key<<"), [ ";
        for(int i=0;i<25;i++){
            output_key2<<ks_all->stecker[i]<<", ";
        }
        output_key2<<ks_all->stecker[25];
        output_key2<<" ]"<<std::endl;
        output_key2<<"加密结果: ";
        encrypt(ks_all,plain,plain.length(),&output_key2);
    }
}