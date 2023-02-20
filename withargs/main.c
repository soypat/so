#include <stdio.h>
#include "dyn.h"

int main(void) {
    puts("running program");
    int a = fibonacci(10);
    printf("fibonacci %d", a);
    return 0;
}