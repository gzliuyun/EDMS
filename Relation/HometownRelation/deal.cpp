#include<iostream>
#include<stdio.h>
#include<string.h>
using namespace std;

const int MAX_NUM = 3219;
char name[MAX_NUM][40];
int id[MAX_NUM];
int fa[MAX_NUM];

int main() {
    freopen("hometownid.txt", "r", stdin);

    for(int i = 0; i < MAX_NUM; i++)
        scanf("%d", &id[i]);

//    for(int i = 0; i < MAX_NUM; i++)
//        printf("%d\n", id[i]);

    freopen("hometown.txt", "r", stdin);
    freopen("ht_dict.py", "w", stdout);
    printf("# -*- coding: utf-8 -*-\n");
    printf("MAX_HT_NUM = 3219\n");
    printf("ht_dict = {\n");
    int curfa = -1;
    for(int i = 0; i < MAX_NUM; i++) {
        char tmp[40];
        scanf("%s", tmp);
        sprintf(name[i], "%s", tmp);
        printf("    \'%s\':\'%d\',\n", name[i], id[i]);
    }
    printf("}\n");

    freopen("ht_list.py", "w", stdout);
    printf("# -*- coding: utf-8 -*-\n");
    printf("ht_list = [\n");
    for(int i = 0; i < MAX_NUM; i++) {
        printf("    \'%s\',\n", name[i]);
    }
    printf("]\n");


    return 0;
}
