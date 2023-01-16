from english_words import get_english_words_set
import json
import os
from sys import platform


path = os.getcwd()
if platform == "linux" or platform == "linux2":
    path = path + "/wordle.json"
elif platform == "darwin":
    path = path + "/wordle.json"
elif platform == "win32":
    path = path + "\wordle.json"

guess = "salet"
result = "wwwmw"

cypher = {}
for count, letter in enumerate(guess):
    cypher[letter] = result[count]

print(cypher)


def trim(words, cypher):

    for count, key in enumerate(cypher.keys()):
        if cypher[key] == "w":
            words = [word for word in words if key not in word]

        if cypher[key] == "c":
            words = [word for word in words if key == word[count]]

        if cypher[key] == "m":
            words = [word for word in words if key in word and key != word[count]]

    return words


if "wordle.json" in os.listdir():
    with open(path, "r", encoding="utf-8") as f:
        words = json.load(f)
else:
    words = list(get_english_words_set(['web2'], lower=True))
    words = [s for s in words if len(s) == 5]


words = trim(words, cypher)

print(words)
print(len(words))

with open(path, "w", encoding="utf-8") as f:
    json.dump(words, f)
