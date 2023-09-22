#include "include.h"
#include <iostream>
#include <fstream>
#include <string>

int main_decrypt(std::ofstream &output_key0, std::ofstream &output_key1, std::ofstream &output_key2, int initial_place){
    output_key1<<"----------initial_place="<<initial_place<<"----------";
    output_key2<<"----------initial_place="<<initial_place<<"----------";

    //step0，即通过环路获得的原始密钥
    int characteristic_array[6]={1,1,0,1,0,0};
    int characteristic_array2[6]={0,1,1,0,0,1};
    bool **key=find_possible_key(6, characteristic_array, initial_place);
    bool **key2=find_possible_key(6, characteristic_array2, initial_place);
    //打印step0获得的密钥
    for(int i=25;i>-1;i--){
        for(int j=25;j>-1;j--){
            if(key[i][j]==1 && key2[i][j]){
                output_key0<<i<<" "<<j<<std::endl;
            }
        }
    }


    //step1，经过相邻环路的筛选，同时构造出完整key的结构
    std::list<Key_Stecker*>* key_stecker_list_pre=step1_select_valid_key(key, key2, initial_place);
    //打印step1获得的密钥
    for(Key_Stecker* ks:*key_stecker_list_pre){
        output_key1<<ks->mid_key<<" "<<ks->quick_key<<std::endl;
    }


    //step2+3，恢复接线板，其中step2是利用crib中的环路恢复，step3是利用crib中的非环路恢复
    std::string plain="wetter";
    std::list<Key_Stecker *> * key_stecker_list=step2_delete_invalid_key(key_stecker_list_pre, plain.length(), characteristic_array, plain, initial_place);
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
        encrypt(ks_all,plain,plain.length(),&output_key2, initial_place);
    }

    return 0;


    // std::ofstream output_key3;
    // output_key3.open("key_test.txt");
    // if(!output_key3.is_open()){
    //     std::cerr<<"无法打开文件"<<std::endl;
    //     return 1;
    // }
    // Key_Stecker* ks_test=new Key_Stecker(13, 4);
    // // ks_test->stecker[1]=4;
    // // ks_test->stecker[4]=1;
    // // ks_test->stecker[2]=19;
    // // ks_test->stecker[19]=2;
    // // ks_test->stecker[10]=17;
    // // ks_test->stecker[17]=10;
    // // ks_test->stecker[11]=22;
    // // ks_test->stecker[22]=11;
    // // ks_test->stecker[14]=15;
    // // ks_test->stecker[15]=14;
    // ks_test->stecker[3]=22;
    // ks_test->stecker[22]=3;
    // ks_test->stecker[4]=20;
    // ks_test->stecker[20]=4;
    // ks_test->stecker[9]=15;
    // ks_test->stecker[15]=9;
    // ks_test->stecker[17]=18;
    // ks_test->stecker[18]=17;
    // ks_test->stecker[19]=21;
    // ks_test->stecker[21]=17;

    // encrypt(ks_test,plain,plain.length(),&output_key3);

    // std::cout<<rotors_and_reflector(1,0,0);
}

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

    //主函数
    for(int i=0;i<26;i++){
        main_decrypt(output_key0, output_key1, output_key2, i);
    }

    output_key0.close();
    output_key1.close();
    output_key2.close();
}