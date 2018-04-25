#include<stdlib.h>
#include<stdio.h>

#define N 100000000

void init(double* p){
    for(int i = 0; i< N; i++){
        p[i] = rand() % 100;
    }
}

int main(int argc, char** argv){
    double* a = malloc(N * sizeof(double)); 
    double* b = malloc(N * sizeof(double));
    int i = 0;

    srand(42);

    init(a);
    init(b);

    double resp = 0.0;
#pragma parallel
    for(i = 0; i<N; i++){
        resp += a[i] * b[i];
    }
    printf("%f\n", resp);
}
