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
how_many_letters_wordle_game = 8


def has_duplicate_letters(word):
    return len(set(word)) != len(word)


def filter_word_list(words, guess, result):

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

# Line 56-81 was written by chatgpt with modifications by me


def most_common_letters(words_list, dupe=bool):
    # Create an empty dictionary to store the letter counts
    letter_count = {}
    for word in words_list:
        for letter in word:
            if letter in letter_count:
                letter_count[letter] += 1
            else:
                letter_count[letter] = 1

    # Create a list of tuples to store the word and common letters count
    common_letters_list = []
    for word in words_list:
        common_letters = 0
        for letter in word:
            if letter_count[letter] > 1:
                common_letters += letter_count[letter]
        common_letters_list.append((word, common_letters))
    # filter the list that contain duplicate letters
    if dupe:
        common_letters_list = [
        word for word in common_letters_list if not has_duplicate_letters(word[0])]
    # Sort the list of tuples by common letters count in descending order
    common_letters_list.sort(key=lambda x: x[1], reverse=True)

    # Return the top three words
    return [word[0] for word in common_letters_list[:3]]


words = open("words_alpha.txt", "r").read().splitlines()
words = [s for s in words if len(s) == how_many_letters_wordle_game]


print(f"Size of wordlist: {len(words)}")
print(f"Possible first guesses:  {most_common_letters(words, True)}")

while True:
    guess = input("Guess: ").lower()
    if has_duplicate_letters(guess):
        continue

    result = input("Result: ").lower()
    if result == "ggggg":
        break
    elif result == "skip":
        continue

    print()
    words = filter_word_list(words, guess, result)
    print(words)
    print()
    next_guess = most_common_letters(words, True)

    if len(next_guess) == 0:
        print("No good guesses!")
        print("Try these instead")
        print(most_common_letters(words, False))
    else:
        print(next_guess)
    print(len(words))
