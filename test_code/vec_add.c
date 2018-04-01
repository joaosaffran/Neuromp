#include<stdio.h>
#include <stdlib.h>

#define N 500000000

void init(unsigned long* vec){
    for(unsigned long i = 0; i< N; i++)
        vec[i] = (unsigned long)rand();
}

int main(int argc, char** argv){
    unsigned long a = 2;
    unsigned long* x = malloc(N * sizeof(unsigned long));
    unsigned long* y = malloc(N * sizeof(unsigned long));
    
    srand(42);
    init(x);
    init(y);
    for(unsigned long i = 0; i< N; i++){
        y[i] = a * x[i] + y[i];
    }
    printf("%lu\n", y[N-1]);

}
