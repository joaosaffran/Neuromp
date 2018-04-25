#include<stdio.h>
#include<stdlib.h>
#include<math.h>

#define K 3
#define N 10000
#define DIM 1000

double euclidean(double* x, double* y, size_t n){
    double resp = 0.0;

    for(size_t i = 0; i< n; i++){
        resp += pow(x[i] - y[i], 2); 
    }

    return sqrt(resp);
}

void init(double** vec, size_t n){
    for(size_t i = 0; i < n; i++){
        vec[i] = (double*)malloc(DIM * sizeof(double));
        for(size_t j = 0; j < DIM; j++){
            vec[i][j] = rand() % 100;
        }
    }
}

int main(int argc, char** argv){
    double** points = (double**)malloc(N * sizeof(double*));
    double** centroids = (double**)malloc(K * sizeof(double*));
    
    int clusters[N];
    int counts[K];

    char changed = 1;

    init(points, N);
    init(centroids, K);
    
    size_t i, j; 
    double dist, point_dist;
    int cluster;
        
    while(changed){
        // Calculating Distances
        changed = 0;
        //printf("RUNNING...\n");
        for(i = 0; i< N; i++){
            dist = 1000000;
            cluster = 0;
            
            for(j = 0; j < K; j++){
                point_dist = euclidean(points[i], centroids[j], DIM);

                if(point_dist < dist){
                    dist = point_dist;
                    cluster = (int)j;
                }
            }
            if(clusters[i] != cluster){
                changed = changed || 1;
                clusters[i] = cluster;
            }
        }

        if(changed == 0){
            break;
        }

        //printf("1\n");
        //Averaging Centroids
        for(i = 0; i<K; i++){
            counts[i] = 0;
            for(j = 0; j<DIM; j++){
                centroids[i][j] = 0.0;
            }
        }
        //printf("2\n");
        for(i = 0; i < N; i++){
                cluster = clusters[i];
                counts[cluster]++;

                for(j = 0; j < DIM; j++){
                    centroids[cluster][j] += points[i][j];
                }
        }
        //printf("3\n");
        
        for(i = 0; i < K; i++){
            for(j = 0; j < DIM; j++){
                centroids[i][j] /= counts[i];
            }
        }
    } 
 /*   for(size_t i = 0; i<K; i++){
        for(size_t j = 0; j<DIM; j++){
            printf(" %f ", centroids[i][j]);
        }
        printf("\n");
    }*/
}
