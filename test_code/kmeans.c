#include<stdio.h>
#include<stdlib.h>
#include<math.h>

#define K 3
#define N 10000
#define DIM 100

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
        for(size_t j = 0; j < DIM; j++)
            vec[i][j] = rand() % 100;
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
    
    while(changed){
        // Calculating Distances
        changed = 0;
        printf("RUNNING...\n");
        
        //#pragma omp parallel for
        for(size_t point = 0; point< N; point++){
            double dist = INFINITY;
            int cluster = 0;
            
            for(size_t centroid = 0; centroid < K; centroid++){
                double point_dist = euclidean(points[point], centroids[centroid], DIM);

                if(point_dist < dist){
                    dist = point_dist;
                    cluster = (int)centroid;
                }
            }
            if(clusters[point] != cluster){
                changed = changed || 1;
                clusters[point] = cluster;
            }
        }

        if(changed == 0)
            break;

        //Averaging Centroids
        for(size_t i = 0; i<K; i++){
            counts[i] = 0;
            for(size_t j = 0; j<DIM; j++){
                centroids[i][j] = 0.0;
            }
        }

        for(size_t point = 0; point < N; point++){
                int cluster = clusters[point];
                counts[cluster]++;

                for(size_t pos = 0; pos < DIM; pos++)
                    centroids[cluster][pos] += points[point][pos];
        }
        
        for(size_t centroid = 0; centroid < K; centroid++)
            for(size_t pos = 0; pos < DIM; pos++)
                centroids[centroid][pos] /= counts[centroid];
    } 
    for(size_t i = 0; i<K; i++){
        for(size_t j = 0; j<DIM; j++){
            printf(" %f ", centroids[i][j]);
        }
        printf("\n");
    }
}
