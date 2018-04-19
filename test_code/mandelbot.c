#include <stdio.h>      /* Standard Library of Input and Output */
#include <complex.h>    /* Standard Library of Complex Numbers */
#include <stdlib.h>

#define max_row 10000
#define max_col 10000

void init(double** p){
    for(int i = 0; i<max_row; i++){
        p[i] = (double*)malloc(max_col * sizeof(double));
    }
}

int main(int argc, char** argv){
    double ** p = (double**)malloc(max_row * sizeof(double*));
    int i,j,k;
    init(p);
    double z, c = 0.0;

    int depth = 80;
//#pragma parallel
#pragma omp parallel for shared(c, z) private(i, j)    
    for(i = 0; i < max_row; i++){
        for(j = 0; j< max_col; j++){
            z = 0;
            c = i + j;

            for(k = 0; k < depth; k++){
                if(cabs(z) >= 2000.0)
                    break;
                z = z*z + c;
            }
            p[i][j] = z;
        }
    }
    printf("%f + i%f\n", creal(p[10][10]), cimag(p[10][10]));
}
