#include "include.h"
#include <iostream>
#include <fstream>
#include <string>

int main_decrypt(std::ofstream &output_key1, std::ofstream &output_key2, int initial_place){
    output_key1<<"----------initial_place="<<initial_place<<"----------"<<std::endl;
    output_key2<<"----------initial_place="<<initial_place<<"----------"<<std::endl;

    //step1，即通过两个环路获得的原始密钥，同时构造出完整key的结构
    int characteristic_array[6]={1,1,0,1,0,0};
    int characteristic_array2[6]={0,1,1,0,0,1};
    bool **key=find_possible_key(6, characteristic_array, initial_place);
    bool **key2=find_possible_key(6, characteristic_array2, initial_place);
    std::list<Key_Stecker*>* key_stecker_list_pre=step1_select_valid_key(key, key2, initial_place);
    //打印step1获得的密钥
    for(Key_Stecker* ks:*key_stecker_list_pre){
        output_key1<<ks->mid_key<<" "<<ks->quick_key<<std::endl;
    }
    //释放内存
    for(int i=0;i<26;i++){
        delete[] key[i];
        delete[] key2[i];
    }
    delete key;
    delete key2;

    //step2+3，恢复接线板，其中step2是利用crib中的环路恢复，step3是利用crib中的非环路恢复
    std::string plain="wetter";
    std::list<Key_Stecker *> * key_stecker_list=step2_delete_invalid_key(key_stecker_list_pre, plain.length(), characteristic_array, plain, initial_place);
    //打印step2+3获得的密钥，此时已经获得满足crib的密钥

    for(Key_Stecker* ks_all:*key_stecker_list){  
        output_key2<<"("<<ks_all->mid_key<<", "<<ks_all->quick_key<<"), [ ";
        for(int i=0;i<25;i++){
            output_key2<<ks_all->stecker[i]<<", ";
        }
        output_key2<<ks_all->stecker[25];
        output_key2<<" ]"<<std::endl;
        output_key2<<"加密结果: ";
        encrypt(ks_all,plain,plain.length(),&output_key2, initial_place);
    }

    int number=key_stecker_list->size();
    //销毁存储密钥的链表
    key_stecker_list_pre->clear();
    key_stecker_list->clear();

    return number;
}

int main(){

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

    int sum=0;
    //主函数
    for(int i=0;i<26;i++){
        sum=sum+main_decrypt(output_key1, output_key2, i);
    }
    std::cout<<sum;

    output_key1.close();
    output_key2.close();
}