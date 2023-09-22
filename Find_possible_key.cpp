#include <list>
#include <string>
#include <iostream>
#include "include.h"

// int QUICK_R[26] = {0, 18, 24, 10, 12, 20, 8, 6, 14, 2, 11, 15, 22, 3, 25, 7, 17, 13, 1, 5, 23, 9, 16, 21, 19, 4};
// int MID_R[26] = {0, 10, 4, 2, 8, 1, 18, 20, 22, 19, 13, 6, 17, 5, 9, 3, 24, 14, 12, 25, 21, 11, 7, 16, 15, 23};
// int T_R[26] = {10, 20, 14, 8, 25, 15, 16, 21, 3, 18, 0, 23, 13, 12, 2, 5, 6, 19, 9, 17, 1, 7, 24, 11, 22, 4};
int QUICK_R[26] = {0, 18, 9, 13, 25, 19, 7, 15, 6, 21, 3, 10, 4, 17, 8, 11, 22, 16, 1, 24, 5, 23, 12, 20, 2, 14};
int MID_R[26] = {0, 5, 3, 15, 2, 13, 11, 22, 4, 14, 1, 21, 18, 10, 17, 24, 23, 12, 6, 9, 7, 20, 8, 25, 16, 19};
int T_R[26] = {10, 20, 14, 8, 25, 15, 16, 21, 3, 18, 0, 23, 13, 12, 2, 5, 6, 19, 9, 17, 1, 7, 24, 11, 22, 4};
int QUICK_R_inv[26] = {0, 18, 24, 10, 12, 20, 8, 6, 14, 2, 11, 15, 22, 3, 25, 7, 17, 13, 1, 5, 23, 9, 16, 21, 19, 4};
int MID_R_inv[26] = {0, 10, 4, 2, 8, 1, 18, 20, 22, 19, 13, 6, 17, 5, 9, 3, 24, 14, 12, 25, 21, 11, 7, 16, 15, 23};

int rotors_and_reflector(int input, int mid_key, int quick_key)
{
    int tmp = 0;
    // 过快速转子
    tmp = (QUICK_R[(input + quick_key) % 26] - quick_key + 26) % 26;
    // 过中速转子
    tmp = (MID_R[(tmp + mid_key) % 26] - mid_key + 26) % 26;
    
    // 过反射器
    tmp = T_R[tmp];
    // 过逆中速转子
    tmp = (MID_R_inv[(tmp+mid_key)%26] - mid_key + 26) % 26;
    // 过逆快速转子
    tmp = (QUICK_R_inv[(tmp+quick_key)%26] - quick_key + 26) % 26;

    return tmp;
}

/**
 * 遍历所有key，找出可能的key
 */
bool **find_possible_key(int loop_length, int *characteristic_array, int initial_place)
{
    // 创建26*26数组以保存key，key[4][4]==1说明(4,4)是其中一个key;
    bool **key = new bool *[26];
    for (int i = 0; i < 26; i++)
    {
        key[i] = new bool[26]();
    }
    // 遍历所有密钥
    for (int mid_key = 25; mid_key > -1; mid_key--)
    {
        for (int quick_key = 25; quick_key > -1; quick_key--)
        {
            // 26条通路
            for (int letter = 0; letter < 26; letter++)
            {
                int quick_key_tmp = quick_key;
                int mid_key_tmp = mid_key;
                int result_tmp = letter;
                // 形成某一条通路
                for (int j = 0; j < loop_length; j++)
                {
                    if (characteristic_array[j] == 1)
                    {
                        result_tmp = rotors_and_reflector(result_tmp, mid_key_tmp, quick_key_tmp);
                        // change *_key_tmp
                        if (quick_key_tmp == initial_place)
                        {
                            mid_key_tmp = (mid_key_tmp + 25) % 26;
                        }
                        quick_key_tmp = (quick_key_tmp + 25) % 26;
                    }
                    else
                    {
                        // change *_key_tmp
                        if (quick_key_tmp == initial_place)
                        {
                            mid_key_tmp = (mid_key_tmp + 25) % 26;
                        }
                        quick_key_tmp = (quick_key_tmp + 25) % 26;
                    }
                }
                // 判断该通路是否成环
                if (result_tmp == letter)
                {
                    key[mid_key][quick_key] = 1;
                    break;
                }
            }
        }
    }
    return key;
}

// 定义构造函数，以便下面的函数使用
Key_Stecker::Key_Stecker(int mid_key, int quick_key)
{
    this->mid_key = mid_key;
    this->quick_key = quick_key;
    for (int i = 0; i < 26; i++)
    {
        stecker[i] = i;
    }
}
/**
 * 利用同一个crib下两个相邻的环路来删除无效key
 *
 */
std::list<Key_Stecker *> *step1_select_valid_key(bool **key, bool **key2, int initial_place)
{
    // 创建链表来存储预完整密钥
    std::list<Key_Stecker *> *key_stecker_list_pre = new std::list<Key_Stecker *>;

    for (int mid_key = 25; mid_key > -1; mid_key--)
    {
        for (int quick_key = 25; quick_key > -1; quick_key--)
        {
            // 本身存在成环通路,下一个也存在成环通路
            if (key[mid_key][quick_key] == 1 && key2[mid_key][quick_key]==1)
            {
                Key_Stecker *ks = new Key_Stecker(mid_key, quick_key);
                key_stecker_list_pre->push_back(ks);
            }
        }
    }
    return key_stecker_list_pre;
}

/**
 * 以下两个小函数均是给下面第三个函数提供帮助的
*/

/**
 * 设置接线板，设置成功（无冲突）返回1.
*/
bool set_stecker(int operand1, int operand2, Key_Stecker *all_ks, int *stecker_help_array){
    if(all_ks->stecker[operand1]==operand2 && all_ks->stecker[operand2]==operand1){
        if(operand1==operand2){
            stecker_help_array[operand1]=1;
        }
        return 1;
    }else if(all_ks->stecker[operand1]==operand1 && all_ks->stecker[operand2]==operand2){
        if(stecker_help_array[operand1]==1 || stecker_help_array[operand2]==1){
            return 0;
        }
        all_ks->stecker[operand1]=operand2;
        all_ks->stecker[operand2]=operand1;
        all_ks->stecker_link_number=all_ks->stecker_link_number+1;
        return 1;
    }else{
        return 0;
    }
}
/**
 * 用不在环中的字母做筛选
*/
bool step3_find_valid_key(char from_letter, int to, int mid_key, int quick_key, int move, Key_Stecker *all_ks, int *stecker_help_array, int initial_place){
    int from=from_letter-'a';

    // change *_key
    for(int i=0;i<move;i++){
        if (quick_key == initial_place )
        {
            mid_key = (mid_key + 25) % 26;
        }
        quick_key = (quick_key + 25) % 26;
    }

    to=rotors_and_reflector(to,mid_key,quick_key);
    return set_stecker(from, to, all_ks, stecker_help_array);
}
/**
 * 恢复接线板同时进行密钥筛选
*/
std::list<Key_Stecker *> *step2_delete_invalid_key(std::list<Key_Stecker *> *key_stecker_list_pre, int loop_length, int *characteristic_array, std::string plain, int initial_place)
{
    // 创建链表来存储可能的完整密钥
    std::list<Key_Stecker *> *key_stecker_list = new std::list<Key_Stecker *>;
    for (Key_Stecker *ks : *key_stecker_list_pre)
    {
        // 找到26条通路中形成环路的通路
        for (int letter = 0; letter < 26; letter++)
        {
            int quick_key_tmp = ks->quick_key;
            int mid_key_tmp = ks->mid_key;
            int result_tmp = letter;

            // 用来存储过程值
            int *result = new int[loop_length]();
            // 形成某一条通路
            for (int j = 0; j < loop_length; j++)
            {
                if (characteristic_array[j] == 1)
                {
                    result[j] = result_tmp;
                    result_tmp = rotors_and_reflector(result_tmp, mid_key_tmp, quick_key_tmp);
                    // change *_key_tmp
                    if (quick_key_tmp == initial_place)
                    {
                        mid_key_tmp = (mid_key_tmp + 25) % 26;
                    }
                    quick_key_tmp = (quick_key_tmp + 25) % 26;
                }
                else
                {
                    // change *_key_tmp
                    if (quick_key_tmp == initial_place)
                    {
                        mid_key_tmp = (mid_key_tmp + 25) % 26;
                    }
                    quick_key_tmp = (quick_key_tmp + 25) % 26;
                }
            }
            // 判断该通路是否成环
            if (result_tmp == letter)
            {      
                // 通路成环，开始恢复stecker
                Key_Stecker *all_ks = new Key_Stecker(ks->mid_key, ks->quick_key);
                //用于辅助诊断接线板是否冲突
                int stecker_help_array[26]={0};
                //用于判断这个完整key是否可以加入到链表中
                bool is_valid=1;
                for (int j = 0; j < loop_length; j++)
                {
                    if (characteristic_array[j] == 1)
                    {
                        int value=plain[j]-'a';
                        is_valid=is_valid & set_stecker(value, result[j], all_ks, stecker_help_array);
                    }
                }
                //这是一个写死的函数，不同crib需要不同的函数，作用是用crib中不在环路内的字母给密钥做筛选
                is_valid=is_valid & step3_find_valid_key('r',result[3],ks->mid_key,ks->quick_key,2,all_ks, stecker_help_array, initial_place);
                is_valid=is_valid & step3_find_valid_key('p',result[1],ks->mid_key,ks->quick_key,4,all_ks, stecker_help_array, initial_place);
                is_valid=is_valid & step3_find_valid_key('r',result[1],ks->mid_key,ks->quick_key,5,all_ks, stecker_help_array, initial_place);
                

                if(is_valid){
                    key_stecker_list->push_back(all_ks);
                }else{
                    delete all_ks;
                }
            }
        }
    }
    return key_stecker_list;
}