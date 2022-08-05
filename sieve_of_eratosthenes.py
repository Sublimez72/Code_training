import json
import argparse


parser = argparse.ArgumentParser(
    description="Displays all the prime numbers less than the supplied number")
parser.add_argument("number", type=int)
parser.add_argument("-t", "--text", help="pipe the output to a textfile")
parser.add_argument(
    "-j", "--json", help="pipe the output to a JSON file as a list")

arg = parser.parse_args()


def SieveOfEratosthenes(num):
    prime = [True for i in range(num+1)]
    primeList = []
    p = 2
    while (p * p <= num):
        if (prime[p] == True):
            for i in range(p * p, num + 1, p):
                prime[i] = False
        p += 1

    for p in range(2, num+1):
        if prime[p]:
            primeList.append(p)

    return primeList


if __name__ == "__main__":

    if arg.text != None:
        with open(arg.text, "w", encoding="utf-8") as f:
            for i in SieveOfEratosthenes(arg.number):
                f.write("{0} \n".format(i))

    elif arg.json != None:
        with open(arg.json, "w", encoding="utf-8") as f:
            json.dump(SieveOfEratosthenes(arg.number), f)

    else:
        print("These are the primes smaller than")
        print("or equeal to", arg.number)

        for prime in SieveOfEratosthenes(arg.number):
            print(prime)
