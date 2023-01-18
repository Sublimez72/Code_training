# A pretty good wordle solver.

# The solver can unfortunatley not deal with words that contain duplicate letters.
# That's why it will give you reccomended guesses that only have unique letters.

# INSTRUCTIONS
# When the program asks for a guess type in what you guessed in your wordle game.
# When the program asks for result type in your result as one string.
# For example. If you guessed the word salet and you got a
# green s
# gray a
# gray l
# yellow e
# green t
# you would type that as: gwwyg

# green = g
# yellow = y
# gray = w

# change this variable if you're playing a custom wordle game with a different number of letters
how_many_letters_wordle_game = 4


def has_duplicate_letters(word):
    return len(set(word)) != len(word)


def trim(words, guess, result):

    temp_tuple = tuple(words)
    for word in temp_tuple:

        for i in range(how_many_letters_wordle_game):
            if result[i] == "w" and guess[i] in word:
                words.remove(word)
                break

            elif result[i] == "g" and guess[i] != word[i]:
                words.remove(word)
                break

            elif result[i] == "y" and guess[i] not in word:
                words.remove(word)
                break

            elif result[i] == "y" and guess[i] == word[i]:
                words.remove(word)
                break

    return words


words = open("words_alpha.txt", "r").read().splitlines()
words = [s for s in words if len(s) == how_many_letters_wordle_game]

first_guesses = []
print("Reccomended first guess: salet")
c = 0
for word in words:
    if not has_duplicate_letters(word):
        c += 1
        first_guesses.append(word)
        if c == 3:
            break
print(f"Size of wordlist: {len(words)}")
print(f"Possible first guesses:  {first_guesses}")

while True:
    guess = input("Guess: ").lower()
    if has_duplicate_letters(guess):
        continue

    result = input("Result: ").lower()
    if result == "ggggg":
        break
    elif result == "skip":
        continue

    print("")
    words = trim(words, guess, result)
    print(words)
    print()
    next_guess = []
    for word in words:
        if not has_duplicate_letters(word):
            next_guess.append(word)

    if len(next_guess) == 0:
        print("No recommended guesses!")
    else:
        print(f"Next Guess? {next_guess}")
    print(len(words))
