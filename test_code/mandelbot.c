#include <stdio.h>      /* Standard Library of Input and Output */
#include <complex.h>    /* Standard Library of Complex Numbers */
#include <stdlib.h>

#define max_row 10000
#define max_col 10000

void init(double complex**p){
    for(int i = 0; i<max_row; i++){
        p[i] = (double complex*)malloc(max_col * sizeof(double complex));
    }
}

int main(int argc, char** argv){
    double complex** p = (double complex**)malloc(max_row * sizeof(double complex*));
    init(p);

    int depth = 80;
    int r = 0;
    
    for(int i = 0; i < max_row; i++){
        for(int j = 0; j< max_col; j++){
            double complex z = 0;
            double complex c = i + j * I;

            for(int k = 0; k < depth; k++){
                if(cabs(z) >= 2000.0)
                    break;
                z = z*z + c;
            }
            p[i][j] = z;
        }
    }

    printf("%f + i%f\n", creal(p[10][10]), cimag(p[10][10]));
}
