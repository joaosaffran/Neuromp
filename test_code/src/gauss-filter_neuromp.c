#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#define PI 3.14159265359	
#define E 2.71828182845904
#define SD 0.8

int imgsize = 4096; 
int masksize = 11;

/*
 * Gaussian filter.
 */

void generate_mask(double *mask)
{
    int half;
    int i, j;
    double sec;
    double first;
    double total;

    first = 1.0/(2.0*PI*SD*SD);
    half = masksize >> 1;
    total = 0;

#define MASK(i, j) \
    mask[(i)*masksize + (j)]

    for (i = -half; i <= half; i++)
    {
        for (j = -half; j <= half; j++)
        {
            sec = -((i*i + j*j)/2.0*SD*SD);
            sec = pow(E, sec);

            MASK(i + half, j + half) = first*sec;
            total += MASK(i + half, j + half);
        }
    }

    for (i = 0 ; i < masksize; i++)
    {
        for (j = 0; j < masksize; j++){
            MASK(i, j) /= total;
        }
    }
}

void init(unsigned char *img){
    int i;              /* Loop index.         */
    for (i = 0; i < imgsize*imgsize; i++){
        img[i] = rand() & 0xff;
    }
}

int main(int argc, char **argv)
{
    double *mask;       /* Mask.               */
    unsigned char *img; /* Image.              */

    srand(42);

    img = malloc(imgsize*imgsize*sizeof(char));

    init(img);

    mask = malloc(masksize*masksize*sizeof(double));
    generate_mask(mask);

    int i, j;
    int half;
    double pixel;
    unsigned char *newimg;
    int imgI, imgJ, maskI, maskJ;

    newimg = malloc(imgsize*imgsize*sizeof(unsigned char));

#define MASK(i, j) \
    mask[(i)*masksize + (j)]

#define IMG(i, j) \
    img[(i)*imgsize + (j)]

#define NEWIMG(i, j) \
    newimg[(i)*imgsize + (j)]

    i = 0; j = 0;
    half = imgsize >> 1;
#pragma omp parallel for shared(half, imgsize, masksize) private(pixel, imgI,imgJ,maskI,maskJ,i,j)
    for (imgI = 0; imgI < imgsize; imgI++)
    {			
        for (imgJ = 0; imgJ < imgsize; imgJ++)
        {
            pixel = 0.0;
            for (maskI = 0; maskI < masksize; maskI++)
            {	
                for (maskJ = 0; maskJ < masksize; maskJ++)
                {
                    i = (imgI - half < 0) ? imgsize-1 - maskI : imgI - half;
                    j = (imgJ - half < 0) ? imgsize-1 - maskJ : imgJ - half;

                    pixel += IMG(i, j)*MASK(maskI, maskJ);
                }
            }

            NEWIMG(imgI, imgJ) = (pixel > 255) ? 255 : (int)pixel;
        }
    }

    free(newimg);

    /* House keeping. */
    free(mask);
    free(img);

    return (0);
}
