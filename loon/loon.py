## this is an empty python source file
## if you are reading this: this file was submitted to accompagny our
## hand written solution;

import sys


if __name__ == '__main__':
    k = range(0, 8, 1);
    ##print(*i)
    print(*([1]*53), end=' ')
    print(*([0]*0))

    print(*([1]*48), end=' ')
    print(*([0]*5))

    print(*([1]*40), end=' ')
    print(*([0]*13))
    
    print(*([1]*32), end=' ')
    print(*([0]*21))
    
    print(*([1]*23), end=' ')
    print(*([0]*30))
    for i in range(0, 395):
        print(*([0]*53))
    
