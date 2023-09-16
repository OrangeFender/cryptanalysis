#include <stdio.h>

int main(){
    int QUICK_R[26] = {0, 10, 4, 2, 8, 1, 18, 20, 22, 19, 13, 6, 17, 5, 9, 3, 24, 14, 12, 25, 21, 11, 7, 16, 15, 23};
    int M[26];
    for (int i=0;i<26;i++){
        M[QUICK_R[i]]=i;
    }
    for(int i=0;i<26;i++){
        printf("%d, ", M[i]);
    }
}