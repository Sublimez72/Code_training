import json
import os
from sys import platform


guess = "goose"
result = "wcwcc"

cypher = {}
for count, letter in enumerate(guess):
    cypher[letter] = result[count]


def paths(path, save=bool):
    if save:
        if platform == "linux" or platform == "linux2":
            path = path + "/wordle.json"
        elif platform == "darwin":
            path = path + "/wordle.json"
        elif platform == "win32":
            path = path + "\wordle.json"
        return path

    if not save:
        if platform == "linux" or platform == "linux2":
            path = path + "/words_alpha.txt"
        elif platform == "darwin":
            path = path + "/words_alpha.txt"
        elif platform == "win32":
            path = path + "\words_alpha.txt"
        return path


def trim(words, cypher):

    for count, key in enumerate(cypher.keys()):
        if cypher[key] == "w":
            words = [word for word in words if key not in word]

        elif cypher[key] == "c":
            words = [word for word in words if key == word[count]]

        elif cypher[key] == "m":
            words = [word for word in words if key in word and key != word[count]]

    return words


path = os.getcwd()
if "wordle.json" in os.listdir():
    path = paths(path, True)
    with open(path, "r", encoding="utf-8") as f:
        words = json.load(f)

else:
    path = paths(path, False)
    words = open(path, "r").read().splitlines()
    words = [s for s in words if len(s) == 5]

words = trim(words, cypher)

print(words)
print(len(words))

path = os.getcwd()
path = paths(path, True)
with open(path, "w", encoding="utf-8") as f:
    json.dump(words, f)
