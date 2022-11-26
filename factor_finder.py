import json
from math import isqrt
import argparse
import time

parser = argparse.ArgumentParser(
    description="Supply the program with a number and it will tell you if it's a prime number or not")
parser.add_argument("path", nargs="?")
args = parser.parse_args()

path = args.path


def jsonLoader():
    with open(path, "r", encoding="utf-8") as f:
        global primes
        primes = json.load(f)


def jsonChecker(num):

    for i in primes:
        if num % i == 0 and num != i:
            return False
        if i >= isqrt(num):
            break

    return True


def efficentChecker(num):
    if num == 2:
        return True

    elif num % 2 == 0:
        return False

    for i in range(3, isqrt(num) + 1, 2):
        if num % i == 0:
            return False

    else:
        return True


def exhaustiveChecker(num):
    factorsFound = False
    factors = []
    for i in range(num):
        try:
            if num % i == 0 and i != 1:
                factors.append(i)
                factorsFound = True
        except ZeroDivisionError:
            pass
        except:
            print("Error")

    if factorsFound == True:
        print(num, "is not a prime, these are all it's factors: ")
        for i in factors:
            print(i)
    else:
        print(num, "is a prime! ")


if __name__ == "__main__":

    if args.path != None and args.path:
        jsonLoader()

    while True:
        try:
            num = int(input("What number do you want to test?: "))
            print("1. Efficent Search (no factors)")
            print("2. Exhaustive Search (all factors)")
            print("3. JSON Search (not 100% for numbers over 50 million but much faster)")
            print("4. Quit")
            mode = int(input())
            if mode == 1:
                start_t = time.perf_counter()
                print(efficentChecker(num))
                end_t = time.perf_counter()
                print(f"Duration of search {end_t - start_t}")
            elif mode == 2:
                start_t = time.perf_counter()
                exhaustiveChecker(num)
                end_t = time.perf_counter()
                print(f"Duration of search {end_t - start_t}")
            elif mode == 3:
                if args.path == None:
                    print("You did not specify a JSON File!")
                else:
                    start_t = time.perf_counter()
                    print(jsonChecker(num))
                    end_t = time.perf_counter()
                    print(f"Duration of search {end_t - start_t}")
            elif mode == 4:
                break
        except ValueError:
            print("Invalid choice!")

        except KeyboardInterrupt:
            print("Type a number and at the next stage press 4 to quit.")
