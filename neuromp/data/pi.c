#include <stdio.h>
long long num_passos = 100000000;
double passo;

double calc(double x){
    return 4.0/(1.0 + x*x);
}

int main(int argc, char** argv){
    long long i, j;
    double pi, soma=0.0;
    passo = 1.0/(double)num_passos;
#pragma neuromp
    for(i=0; i < num_passos; i+=5){
        for(j = i; j <= i + 5; j++){
            soma += calc((j + 0.5)*passo);
        }
    }

    pi = soma*passo;

    printf("O valor de PI é: %f\n", pi);
    return 0;
}
