#include<stdio.h>
#include<stdlib.h>

#define N 10000 

void init(char** mat){
    for(size_t i = 0; i< N; i++){
        mat[i] = (char*)malloc(N * sizeof(char));
        for(size_t j = 0; j< N; j++){
            mat[i][j] = rand() % 2;
        }
    }
}

int calcNeigh(char** mat, int i, int j){
    int resp = 0;
    for(int ii = i-1; ii < i+1; ii++ )
        for(int jj = j-1; jj < j+1; jj++ )
            resp += mat[ii][jj];
    return resp;
}

void show(char** mat){
    printf("\n>>>\n");
    for(size_t i = 1; i< N-1; i++){
        for(size_t j = 1; j<N-1; j++){
            if(mat[i][j] == 1)
                printf("*");
            else
                printf(" ");
        }
        printf("\n");
    }
}

int main(int argc, char** argv){
    char** mat = malloc(N * sizeof(char*));
    char** new_mat = malloc(N * sizeof(char*));

    int num_neigh;
    size_t i, j;
    init(mat);
    init(new_mat);

#pragma omp parallel for shared(mat) private(i, j, num_neigh)
    for(i = 1; i< N-1; i++){
        for(j = 1; j<N-1; j++){
            num_neigh = calcNeigh(mat, i, j);        

            if(mat[i][j] == 1 && !(num_neigh == 2 || num_neigh == 3))
            {
                new_mat[i][j] = 0;
            }else{
                new_mat[i][j] = 1;
            }
            
            if(mat[i][j] == 0 && num_neigh == 3)
            {
                new_mat[i][j] = 1;
            }else{
                new_mat[i][j] = 0;
            }
        }
    }

//    show(new_mat);
}
