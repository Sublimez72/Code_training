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


def filter_word_list(words, guess, result):

    temp_dict = {}

    for index, letter in enumerate(guess):
        if letter not in temp_dict:
            temp_dict[letter] = result[index]
        elif letter in temp_dict:
            temp_dict[letter+str(index)] = result[index]

    print(temp_dict)

    temp_tuple = tuple(words)
    for word in temp_tuple:

        for i in range(how_many_letters_wordle_game):


            if result[i] == "w" and guess[i] in word:
                for z in range(how_many_letters_wordle_game):
                    if guess[i]+str(z) in temp_dict and temp_dict[guess[i]+str(z)] != "w":
                        if word[i] == guess[i]:
                            words.remove(word)
                        break
                else:
                    words.remove(word)
                break

            elif result[i] == "g" and guess[i] != word[i]:
                count = 1
                for z in range(how_many_letters_wordle_game):
                    if guess[i] + str(z) in temp_dict and temp_dict[guess[i]+str(z)] == "g":
                        count += 1
                    
                if word.count(guess[i]) != count:
                    words.remove(word)
                    break
                
                elif word.count(guess[i]) == count and guess[i] != result[i]:
                    words.remove(word)
                    break


            elif result[i] == "y" and guess[i] not in word:
                words.remove(word)
                break

            elif result[i] == "y" and guess[i] == word[i]:
                words.remove(word)
                break

    return words


# Line 56-81 was written by chatgpt


def most_common_letters(words_list):
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

    # Sort the list of tuples by common letters count in descending order
    common_letters_list.sort(key=lambda x: x[1], reverse=True)

    # Return the top three words
    return [word[0] for word in common_letters_list[:3]]


words = open("words_alpha.txt", "r").read().splitlines()
words = [s for s in words if len(s) == how_many_letters_wordle_game]


print(f"Size of wordlist: {len(words)}")
print(f"Possible first guesses:  {most_common_letters(words)}")

while True:
    guess = input("Guess: ").lower()

    result = input("Result: ").lower()
    if result == "skip":
        continue

    print()
    words = filter_word_list(words, guess, result)
    print(words)
    print()
    next_guess = most_common_letters(words)

    if len(next_guess) == 0:
        print("No recommended guesses!")
    else:
        print(next_guess)
    print(len(words))
