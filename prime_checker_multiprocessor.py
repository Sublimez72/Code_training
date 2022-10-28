from math import ceil, isqrt
import multiprocessing
import time

# Big primes
num = 170141183460469231731687303715884105727
#num = 67280421310721
num = 1871677000017371



def factor_finder(i):
    if num % i == 0:
            return i
    else:
        return False



if __name__ == '__main__':

    with multiprocessing.Pool() as p:
        start_t = time.perf_counter()
        for i in p.map_async(factor_finder, range(2, ceil(isqrt(num)))).get():
            if type(i) == int:
                end_t = time.perf_counter()
                print(f"{num} is NOT a prime!\nDuration of search: {end_t - start_t}")
                p.terminate()
                break
        else:
            end_t = time.perf_counter()
            print(f"{num} IS a prime!\nDuration of search: {end_t - start_t}")
