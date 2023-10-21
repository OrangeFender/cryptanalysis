#include<iostream>
#include<vector>
#include<bitset>
using namespace std;

int _add(int a, int b){
    //0+k=k
    if(a==0)
        return b;
    if(b==0)
        return a;
    //1+1*=2*
    if((a==1 && b==2) || (a==2 && b==1))
        return 3;
    //others
    return 4;
}
int _mul(int a, int b){
    //0*k=0
    if(a==0 || b==0)
        return 0;
    //k*1=k
    if(b==1)
        return a;
    //1* * 1f=1, 1*1f=1
    if(a==1 || a==2)
        return 1;
    //others
    return 4;
}
bool is_complement(vector<int> &a, vector<int> &b, int &pos){
    for (int i = 0; i < a.size();i++){
        switch (a[i])
        {
        case 0:
            if(b[i]==1||b[i]==2)//1 1*
            {
                pos = i+1;
                return true;
            }
            break;
        case 1:
            if (b[i] == 0) // 1 1*
            {
                pos = i + 1;
                return true;
            }
            break;
        case 2:
            if (b[i] == 0||b[i]==2||b[i]==3) // 1 1*
            {
                pos = i + 1;
                return true;
            }
            break;
        case 3:
            if (b[i] == 2) // 1 1*
            {
                pos = i + 1;
                return true;
            }
            break;
        default:
            break;
        }
    }
    return false;
}
bool all_t(vector<int> &v){
    for (int i = 0; i < v.size(); i++){
        if(v[i]!=4)
            return false;
    }
    return true;
}
void rf_calculate(vector<int> &currentState, vector<vector<int>> &interState, int (&ED)[4][4]){
    while (1)
    {
        vector<int> nextState;
        for (int i = 0; i < 4; i++)
        {
            int sum = 0;
            for (int j = 0; j < 4; j++)
            {
                sum = _add(sum, _mul(currentState[j], ED[j][i]));
            }
            nextState.push_back(sum);
        }
        currentState = nextState;
        if(all_t(currentState))break;
        else
            interState.push_back(currentState);
    }
}
bool find_contradiction(vector<vector<int>> headState, vector<vector<int>> tailState, int &tmpmaxlen)
{
    int maxlen = 0;
    int max_con_pos = 0;
    int maxi = 0, maxj = 0;
    vector<int> max_head;
    vector<int> max_tail;
    for (int i = 0; i < headState.size(); i++){
        for (int j = 0; j < tailState.size(); j++){
            int con_pos = 0;
            if(is_complement(headState[i], tailState[j], con_pos)){
                int len = i + j + 2;
                if (len > maxlen){
                    maxlen = len;
                    max_con_pos = con_pos;
                    maxi = i;
                    maxj = j;
                    max_head = headState[i];
                    max_tail = tailState[j];
                }
            }
        }
    }
    if(maxlen>0){
        tmpmaxlen = maxlen;
        cout << "找到最长" << maxlen << "轮不可能差分" << endl;
        for (int i = 0; i <= maxi; i++)
        {
            for (auto &ele : headState[i])
            {
                cout << ele << ", ";
            }
            cout << endl;
        }
        cout << "在第" << max_con_pos << "个元素上找到矛盾点" << endl;
        for (int i = maxj; i >=0; i--)
        {
            for (auto &ele : tailState[i])
            {
                cout << ele << ", ";
            }
            cout << endl;
        }
        cout << endl;
        return true;
    }else{
        return false;
    }
}
int main(){
    int E[4][4] = {
        {2, 0, 0, 1},
        {1, 0, 0, 0},
        {0, 1, 2, 0},
        {0, 0, 1, 0}};
    int D[4][4] = {
        {0, 1, 0, 0},
        {0, 0, 1, 2},
        {0, 0, 0, 1},
        {1, 2, 0, 0}};

    cout << "0:0    1:1    2:1*    3:2*    4:t(≥2)" << endl;
    vector<int> head, tail;
    //手动搜索
    // cout << "输入头差分：";
    // int i = 4;
    // int tmp;
    // while (i--)
    // {
    //     cin >> tmp;
    //     head.push_back(tmp);
    // }
    // cout << "输入尾差分：";
    // i = 4;
    // while (i--)
    // {
    //     cin >> tmp;
    //     tail.push_back(tmp);
    // }
    
    //自动化搜索
    int maxlen = 0;
    for (int i = 1; i < 16;i++){//遍历头差分，不考虑（0,0,0,0）
        bitset<4> bits_head(i);
        head.clear();
        for (int k = 0; k < 4;k++){
            if(bits_head[k])
                head.push_back(2);
            else{
                head.push_back(0);
            }
        }
        for (int j = 1; j < 16; j++) // 遍历尾差分，不考虑（0,0,0,0）
        {
            bitset<4> bits_tail(j);
            tail.clear();
            for (int k = 0; k < 4; k++)
            {
                if (bits_tail[k])
                    tail.push_back(2);
                else
                {
                    tail.push_back(0);
                }
            }
            cout << "头差分：";
            for (auto &ele : head)
            {
                cout << ele << ", ";
            }
            cout << endl;
            cout << "尾差分：";
            for (auto &ele : tail)
            {
                cout << ele << ", ";
            }
            cout << endl;
            
            vector<vector<int>> headState;
            vector<vector<int>> tailState; // 两个集合用于存储传播过程可能情况
            vector<int> curhead(head);
            vector<int> curtail(tail);
            rf_calculate(curhead, headState, E);
            rf_calculate(curtail, tailState, D);

            int tmpmaxlen = 0;
            bool flag = find_contradiction(headState, tailState, tmpmaxlen);
            if(!flag){
                cout << "未找到不可能差分" << endl<<endl;
            }else{
                if (tmpmaxlen > maxlen){
                    maxlen = tmpmaxlen;
                }
            }
        }
    }
    cout << "所有情况下，最长不可能差分的长度为：" << maxlen << endl;
    return 0;
}