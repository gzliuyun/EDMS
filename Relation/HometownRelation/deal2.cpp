#include<iostream>
#include<stdio.h>
#include<string.h>
using namespace std;

const int MAX_NUM = 3219;
char id[MAX_NUM][40];
int index[MAX_NUM];

int main() {
    freopen("hometownid.txt", "r", stdin);
    freopen("ht_id_dict.py", "w", stdout);

    printf("# -*- coding: utf-8 -*-\n");
    printf("ht_id_dict = {\n");

    for(int i = 0; i < MAX_NUM; i++)
        scanf("%s", &id[i]);

    for(int i = 0; i < MAX_NUM; i++)
        printf("    \'%s\':\'%d\',\n", id[i], i);
    printf("}\n");
    return 0;
}
