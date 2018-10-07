#include<iostream>
#include<stdio.h>
#include<string.h>
using namespace std;

char str[1000];

int main() {

	freopen("align_recorde.txt", "r", stdin);
	freopen("new_recode.txt", "w", stdout);

    while(gets(str)) {
        int len = strlen(str);
        int tail = 0;
        while(tail < len) {
            putchar(str[tail]);
            if(str[tail] == '}') {
                putchar('\n');
                break;
            }
            tail++;
        }
    }

	return 0;
}
