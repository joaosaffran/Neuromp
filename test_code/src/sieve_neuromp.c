/*
 * Adapted from: http://w...content-available-to-author-only...s.org/sieve-of-eratosthenes
 */

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <math.h>
#include <time.h>

int main()
{
    int n = 100000000;

    // Create a boolean array "prime[0..n]" and initialize
    // all entries it as true. A value in prime[i] will
    // finally be false if i is Not a prime, else true.
    int primes = 0; 
    bool *prime = (bool*) malloc((n+1)*sizeof(bool));
    int sqrt_n = sqrt(n);

    memset(prime, true,(n+1)*sizeof(bool));

    int i, p;
    
#pragma omp parallel for private(p, i)
    for (p=2; p <= sqrt_n; p++)
    {
        // If prime[p] is not changed, then it is a prime
        if (prime[p] == true)
        {
            // Update all multiples of p
            for (i=p*2; i<=n; i += p){
                prime[i] = false;
            }
        }
    }

    // count prime numbers
    for (p=2; p<=n; p++){
        if (prime[p]){
            primes++;
        }
    }

    printf("%d\n",primes);
    return 0;
} 
