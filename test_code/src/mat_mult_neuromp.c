#include <stdio.h>
#include <stdlib.h>

#define NRA 756                 /* number of rows in matrix A */
#define NCA 756                 /* number of columns in matrix A */
#define NCB 756                  /* number of columns in matrix B */

void init(double** mat, int rows, int cols){
    for (int i=0; i<rows; i++){
        mat[i] = malloc(cols * sizeof(double));
        for (int j=0; j<cols; j++){
            mat[i][j] = i+j;
        }
    }
}


int main (int argc, char *argv[]) 
{
    int i, j, k;
    
    double** a = malloc(NRA * sizeof(double*));           /* matrix A to be multiplied */
    double** b = malloc(NCA * sizeof(double*));           /* matrix B to be multiplied */
    double** c = malloc(NRA * sizeof(double*));           /* result matrix C */

    init(a, NRA, NCA);
    init(b, NCA, NCB);
    init(c, NRA, NCB);

#pragma omp parallel for private(i, j, k)
    for (i=0; i<NRA; i++){
        for(j=0; j<NCB; j++){       
            for (k=0; k<NCA; k++){
                c[i][j] += a[i][k] * b[k][j];
            }
        }
    }

/*    for (i=0; i<NRA; i++)
    {
        for (j=0; j<NCB; j++){ 
            printf("%6.2f   ", c[i][j]);
        }
        printf("\n"); 
    }*/

}

