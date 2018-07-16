# NeurOMP
NeurOMP is a tool for automatically parallelize a C code using Reinforcement Learning.

## Description
NeurOMP uses the [QLearning](https://en.wikipedia.org/wiki/Q-learning) algorithm as an optimizer to find the best [OpenMP](https://www.openmp.org/) pragma capable of making a C Code For Loop run in parallel.

## Installation 
Make sure you have g++ and OpenMP correctly installed on your system.
After that run inside NeurOMP folder:
```
pip install -r requirements.txt
pip install -e .
```
## Usage
NeurOMP requires the user to specify which loop it should become parallel.
For doing so use ```#pragma neuromp``` on the For Loop that can be parallelized.
For example:
```
#include <stdio.h>
long long num_passos = 10000000000;
double passo;

int main(int argc, char** argv){
    long long i;
    double x, pi, soma=0.0;
    passo = 1.0/(double)num_passos;
    
    #pragma neuromp
    for(i=0; i < num_passos; i++){
        x = (i + 0.5)*passo;
        soma += 4.0/(1.0 + x*x);
    }

    pi = soma*passo;

    printf("O valor de PI é: %f\n", pi);
    return 0;
}

```
After that you should write a python script with the following content ( let's suppose that the above file is called pi.c):
```
from neuromp.model.q_learn import QLearn
from neuromp.preprocessing.code import Code, VarStates

optim = QLearn(Code('pi.c'))
optim.fit()
```
After that run the script with default python:
```
python script.py
```
And it is done, you should get your Loop Parallelized!

## Notes
- NeurOMP still have some issues when parsing C code. All the contributors are working to solve this issue as soon as possible.
- NeurOMP require to run the C program in order to optimize the Loop Parallelization. Another open issue, it can't compile multiple files at once. This is already being fix. 
