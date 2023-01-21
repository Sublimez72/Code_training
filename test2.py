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
how_many_letters_wordle_game = 7

# erasion
# ygwgwww

# dressed
# wgggwyw

# correct
# presume


def has_duplicate_letters(word):
    return len(set(word)) != len(word)


def filter_word_list(words, guess, result):
    temp_dict = {}

    for index, letter in enumerate(guess):
        if letter not in temp_dict:
            temp_dict[letter] = result[index]
        elif letter in temp_dict:
            temp_dict[letter+str(index)] = result[index]

    temp_tuple = tuple(words)
    for word in temp_tuple:

        for i in range(how_many_letters_wordle_game):

            if word: print("1", i)
            if result[i] == "w" and guess[i] in word:
                removed = False
                for z in range(how_many_letters_wordle_game):
                    if guess[i]+str(z) in temp_dict and temp_dict[guess[i]+str(z)] != "w" or temp_dict[guess[i]] != "w":
                        if word[i] == guess[i]:
                            if word: print("w1", i)
                            removed = True
                            words.remove(word)
                            break
                    elif guess[i] + str(z) not in temp_dict:
                        if word: print("w2", i)
                        removed = True
                        words.remove(word)
                        break
                    if word: print("break", i, guess[i], result[i], word[i])
                    break
                if removed:
                    break

            if word: print("2", i)
            elif result[i] == "g" and guess[i] != word[i]:
                count = 1
                for z in range(how_many_letters_wordle_game):
                    if guess[i] + str(z) in temp_dict and temp_dict[guess[i]+str(z)] == "g":
                        count += 1

                if word.count(guess[i]) != count:
                    if word: print("g1", i)
                    words.remove(word)
                    break

                elif word.count(guess[i]) == count and guess[i] != result[i]:
                    if word: print("g2", i)
                    words.remove(word)
                    break

            if word: print("3", i)
            elif result[i] == "y" and guess[i] not in word:
                if word: print("y1", i)
                words.remove(word)
                break

            if word: print("4", i)
            elif result[i] == "y" and guess[i] == word[i]:
                if word: print("y2", i)
                words.remove(word)
                break

            if word: print("5", i)
            elif result[i] == "y":
                count = 1
                for z in range(how_many_letters_wordle_game):
                    if guess[i] + str(z) in temp_dict and temp_dict[guess[i]+str(z)] == "y":
                        count += 1

                if word.count(guess[i]) < count:
                    if word: print("y3", i)
                    words.remove(word)
                    break

                elif word.count(guess[i]) == count and guess[i] != result[i]:
                    if word: print("y4", i)
                    words.remove(word)
                    break
            if word: print("end", i)
    return words

# Line 56-81 was written by chatgpt


def most_common_letters(words_list, dupe):
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

    result = input("Result: ").lower()
    if result == "skip":
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
