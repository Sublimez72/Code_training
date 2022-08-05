import argparse
import random

parser = argparse.ArgumentParser(
    description="Takes a string and creates a random anagram.")

parser.add_argument("string")

args = parser.parse_args()


def anagram(string):
    str_list = []

    for i in range(len(args.string)):
        str_list.append(args.string[i])

    random.shuffle(str_list)

    output_string = ""
    for i in str_list:
        output_string += i
    return output_string.lower()


print(anagram(args.string))
