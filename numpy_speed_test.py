import numpy as np
import timeit



def for_loop_test(num=10_000_000):
    s = 0
    for s in range(num):
        s += 1
    return s

def while_loop_test(num=10_000_000):
    s = 0
    i = 0
    while i < num:
        s += i
        i += 1
    return s

def built_in_test(num=10_000_000):
    return sum(range(num))

def numpy_test(num=10_000_000):
    return np.sum(np.arange(num))


print("For loop\t\t", timeit.timeit(for_loop_test, number=1))
print("While loop\t\t", timeit.timeit(while_loop_test, number=1))
print("Built in methods\t\t", timeit.timeit(built_in_test, number=1))
print("Numpy\t\t", timeit.timeit(numpy_test, number=1))