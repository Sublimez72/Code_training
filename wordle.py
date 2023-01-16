import json
import os
from sys import platform


how_many_letters_wordle_game = 5


# salet
guess = "reave"
result = "wwmwc"


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


def trim(words, guess, result):

    temp_tuple = tuple(words)
    for word in temp_tuple:

        for i in range(how_many_letters_wordle_game):
            if result[i] == "w" and guess[i] in word:
                words.remove(word)
                break

            elif result[i] == "c" and guess[i] != word[i]:
                words.remove(word)
                break

            elif result[i] == "m" and guess[i] not in word:
                words.remove(word)
                break

            elif result[i] == "m" and guess[i] == word[i]:
                words.remove(word)
                break

    return words


path = os.getcwd()
if "wordle.json" in os.listdir():
    path = paths(path, True)
    with open(path, "r", encoding="utf-8") as f:
        words = json.load(f)

else:
    path = paths(path, False)
    words = open(path, "r").read().splitlines()
    words = [s for s in words if len(s) == how_many_letters_wordle_game]

words = trim(words, guess, result)


print(words)
print(len(words))


path = os.getcwd()
path = paths(path, True)
with open(path, "w", encoding="utf-8") as f:
    json.dump(words, f)
