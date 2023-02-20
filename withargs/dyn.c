#include<stdio.h>

int fibonacci(int n) {
    int a = 0;
    int b = 1;
    int aux;
    for (int i=0; i<n; i++) {
        aux = a;
        a = b;
        b = aux + b;
    }
    return a;
}
