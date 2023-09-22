#include <iostream>
#include <list>
#include <string>
#include <fstream>
#include "include.h"


/**
 * 寻找crib
 * 返回crib链表，每个节点用string存储crib中的密文
 */
std::list<std::string>* find_crib(std::string plain, std::string cipher){
    //创建一个用于存储crib的链表
    std::list<std::string>* crib_list=new std::list<std::string>;

    //获取长度
    unsigned int p_length=plain.length();
    unsigned int c_length=cipher.length();
	unsigned int loop_times=c_length-p_length+1;

    //寻找crib
    for(int i=0;i<loop_times;i++){
        std::string sub_cipher=cipher.substr(i,p_length);
		int is_valid=1;
        for(int j=0;j<p_length;j++){
            if (plain[j]==sub_cipher[j]){
                is_valid=0;
                continue;
            } 
        }
        if(is_valid){
            crib_list->push_back(sub_cipher);
        }
	}

    //返回crib链表
    return crib_list;
}

/**
 * find_loop()的辅助函数
*/
bool find_loop_helper(unsigned int origin_index, unsigned int current_index, unsigned int crib_length, std::string origin_array, std::string target_array, int * characteristic_array){
    unsigned int loop_times=crib_length;
    for(int i=current_index+1;i<loop_times;i++){
        //判断新的一列是否能接上上一列
        if(origin_array[i]==target_array[current_index]){
            //判断是否闭环
            if(target_array[i]==origin_array[origin_index]){
                characteristic_array[i]=1;
                return 1;
            //没有闭环，继续向深处寻找
            }else{
                if(i==crib_length){
                    return 0;
                }
                if(find_loop_helper(origin_index, i, crib_length, origin_array, target_array, characteristic_array)){
                    characteristic_array[i]=1;
                    return 1;
                }
            }
        }
    }
    return 0;
}

/**
 * 寻找crib里面的环路loop
 * 返回loop链表，每个节点表示一个loop
 * 每个loop用与明文长度相同的int数组表示，这个数组成为特征数组，数值仅取0、1，某列元素取1时，表示此crib中，该列在当前loop中
*/
std::list<int*>* find_loop(std::string crib_plain, std::string crib_cipher){
    //创建一个用于存储环路的链表
    std::list<int*>* loop_list=new std::list<int*>;

    //环路最小长度为2，因此循环次数为crib长度减去1
    unsigned int crib_length=crib_plain.length();
    unsigned int loop_times=crib_length-1;

    //寻找环路，当找到环路时，将环路的特征数组添加到链表
    for(int i=0;i<loop_times;i++){
        int * characteristic_array=new int[crib_length]();
        if(find_loop_helper(i, i, crib_length, crib_plain, crib_cipher, characteristic_array)){
            characteristic_array[i]=1;
            loop_list->push_back(characteristic_array);
        }else{
            delete characteristic_array;
        }
    }

    return loop_list;
}

int find_crib_and_loop_main(std::string plain, std::string cipher){
    //打开文件用于存储结果
    std::ofstream output_file;
    output_file.open("crib_and_loop.txt");
    if(!output_file.is_open()){
        std::cerr<<"无法打开文件"<<std::endl;
        return 1;
    }

    //获得所有crib
    std::list<std::string>* crib_list=find_crib(plain, cipher);
    output_file<<"crib:"<<std::endl;
    output_file<<"plain is :"<<std::endl<<plain<<std::endl;
    output_file<<"=============="<<std::endl;

    //对每对crib尝试破解
    for(std::string& crib_cipher: *crib_list){
        output_file<<"a cipher is:"<<std::endl;
        output_file<<crib_cipher<<std::endl;
        

        //寻找该crib的环路
        int loop_times=plain.length();
        std::list<int*>* loop_list=find_loop(plain, crib_cipher);

        //打印环路，一行明文，一行密文
        for(int* loop: *loop_list){
            output_file<<"--------------"<<std::endl;
            output_file<<"a loop in which is:"<<std::endl;

            for(int i=0;i<loop_times;i++){
                if(loop[i]==0){
                    output_file<<"*";
                }else{
                    output_file<<plain[i];
                }
            }
            output_file<<std::endl;
            for(int i=0;i<loop_times;i++){
                if(loop[i]==0){
                    output_file<<"*";
                }else{
                    output_file<<crib_cipher[i];
                }
            }
            output_file<<std::endl;
        }
        

        output_file<<std::endl;
    }
    
    output_file.close();
    return 0;
}

int main(){
    std::string plain="wetter";
    std::string cipher="betrwpeer";
    find_crib_and_loop_main(plain, cipher);
}
