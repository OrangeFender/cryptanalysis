#include <list>
#include "include.h"

//int QUICK_R[26] = {0, 18, 24, 10, 12, 20, 8, 6, 14, 2, 11, 15, 22, 3, 25, 7, 17, 13, 1, 5, 23, 9, 16, 21, 19, 4};
//int MID_R[26] = {0, 10, 4, 2, 8, 1, 18, 20, 22, 19, 13, 6, 17, 5, 9, 3, 24, 14, 12, 25, 21, 11, 7, 16, 15, 23};
//int T_R[26] = {10, 20, 14, 8, 25, 15, 16, 21, 3, 18, 0, 23, 13, 12, 2, 5, 6, 19, 9, 17, 1, 7, 24, 11, 22, 4};
int QUICK_R[26]={0, 18, 9, 13, 25, 19, 7, 15, 6, 21, 3, 10, 4, 17, 8, 11, 22, 16, 1, 24, 5, 23, 12, 20, 2, 14};
int MID_R[26]={0, 5, 3, 15, 2, 13, 11, 22, 4, 14, 1, 21, 18, 10, 17, 24, 23, 12, 6, 9, 7, 20, 8, 25, 16, 19};
int T_R[26] = {10, 20, 14, 8, 25, 15, 16, 21, 3, 18, 0, 23, 13, 12, 2, 5, 6, 19, 9, 17, 1, 7, 24, 11, 22, 4};
int QUICK_R_inv[26]={0, 18, 24, 10, 12, 20, 8, 6, 14, 2, 11, 15, 22, 3, 25, 7, 17, 13, 1, 5, 23, 9, 16, 21, 19, 4};
int MID_R_inv[26]={0, 10, 4, 2, 8, 1, 18, 20, 22, 19, 13, 6, 17, 5, 9, 3, 24, 14, 12, 25, 21, 11, 7, 16, 15, 23};

int rotors_and_reflector(int input, int mid_key, int quick_key){
    int tmp=0;
    //过快速转子
    tmp=(QUICK_R[(input+quick_key)%26]-quick_key+26)%26;
    //过中速转子
    tmp=(MID_R[(tmp+mid_key)%26]-mid_key+26)%26;
    //过反射器
    tmp=T_R[tmp];
    //过逆中速转子
    tmp=(MID_R_inv[tmp]-mid_key+26)%26;
    //过逆快速转子
    tmp=(QUICK_R_inv[tmp]-quick_key+26)%26;

    return tmp;
}


/**
 * 遍历所有key，找出可能的key
*/
bool ** find_possible_key(int loop_length, int * characteristic_array){
    //创建26*26数组以保存key，key[4][4]==1说明(4,4)是其中一个key;
    bool **key = new bool*[26];
    for(int i=0;i<26;i++){
        key[i]=new bool[26]();
    }
    //遍历所有密钥
    for(int mid_key=25;mid_key>-1;mid_key--){
        for(int quick_key=25;quick_key;quick_key--){
            //26条通路
            for(int letter=0;letter<26;letter++){
                int quick_key_tmp=quick_key;
                int mid_key_tmp=mid_key;
                int result_tmp=letter;
                //形成某一条通路
                for(int j=0;j<loop_length;j++){
                    if(characteristic_array[j]==1){
                        result_tmp=rotors_and_reflector(result_tmp, mid_key_tmp, quick_key_tmp);
                        //change *_key_tmp
                        if(quick_key_tmp==0){
                            mid_key_tmp=(mid_key_tmp+25)%26;
                        }
                        quick_key_tmp=(quick_key_tmp+25)%26;
                    }else{
                        //change *_key_tmp
                        if(quick_key_tmp==0){
                            mid_key_tmp=(mid_key_tmp+25)%26;
                        }
                        quick_key_tmp=(quick_key_tmp+25)%26;
                    }
                }
                //判断该通路是否成环
                if(result_tmp==letter){
                    key[mid_key][quick_key]=1;
                    break;
                }


            }
        }
    }
    return key;
}

//定义构造函数，以便下面的函数使用
Key_Stecker::Key_Stecker(int mid_key, int quick_key){
        key[0]=mid_key;
        key[1]=quick_key;
        for(int i=0;i<26;i++){
            stecker[i]=i;
        }
    }
/**
 * 利用同一个crib下两个相邻的环路来删除无效key
 * 
*/
std::list<Key_Stecker*>* step1_select_valid_key(bool **key){
    //创建链表来存储完整密钥
    std::list<Key_Stecker*> *key_stecker_list=new std::list<Key_Stecker*>;

    for(int mid_key=25;mid_key>-1;mid_key--){
        for(int quick_key=25;quick_key>-1;quick_key--){
            //本身存在成环通路
            if(key[mid_key][quick_key]==1){
                //change *_key_tmp
                int quick_key_tmp=quick_key;
                int mid_key_tmp=mid_key;
                if(quick_key_tmp==0){
                    mid_key_tmp=(mid_key_tmp+25)%26;
                }
                quick_key_tmp=(quick_key_tmp+25)%26;
                //下一个也存在成环通路
                if(key[mid_key_tmp][quick_key_tmp]==1){
                    Key_Stecker *sk=new Key_Stecker(mid_key,quick_key);
                    key_stecker_list->push_back(sk);
                }
            }
        }
    }
    return key_stecker_list;
}

void delete_invalid_key_step2(bool **key){
    
}