#include<stdio.h>
#include <stdlib.h>

#define N 100000000

void init(unsigned long* vec){
    for(unsigned long i = 0; i< N; i++){
        vec[i] = (unsigned long)rand();
    }
}

int main(int argc, char** argv){
    unsigned long* x = malloc(N * sizeof(unsigned long));
    unsigned long* y = malloc(N * sizeof(unsigned long));
    unsigned long i = 0;
    unsigned long a = 2;

    srand(42);
    init(x);
    init(y);
    for(i = 0; i< N; i++){
        y[i] += a * x[i];
    }
    
    printf("%lu\n", y[N-1]);
}
