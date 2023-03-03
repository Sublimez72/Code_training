# A pretty good wordle solver.


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
how_many_letters_wordle_game = 5


def has_duplicate_letters(word):
    return len(set(word)) != len(word)


def count_non_w(guess, result, index):
    letter = guess[index]
    count = 0
    for i, c in enumerate(result):
        if i == index:
            continue
        if guess[i] == letter and c != 'w':
            count += 1
    return count


def filter_word_list(words, guess, result):

    temp_tuple = tuple(words)
    for word in temp_tuple:

        for i in range(how_many_letters_wordle_game):

            if result[i] == "w":
                count_non_w_result = count_non_w(guess, result, i)

                if word.count(guess[i]) != count_non_w_result:
                    words.remove(word)
                    break
                if word[i] == guess[i]:
                    words.remove(word)
                    break

            elif result[i] == "g" and guess[i] != word[i]:
                words.remove(word)
                break

            elif result[i] == "y":
                count_non_w_result = count_non_w(guess, result, i) + 1

                if word.count(guess[i]) < count_non_w_result:
                    words.remove(word)
                    break
                if word[i] == guess[i]:
                    words.remove(word)
                    break

    return words

# Line 56-82 was written by chatgpt with modifications by me


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

if how_many_letters_wordle_game != 5:
    words = open("wordle/words_alpha.txt", "r").read().splitlines()
    words = [s for s in words if len(s) == how_many_letters_wordle_game]
else:
    words = open("wordle/words.txt", "r").read().splitlines()

print(f"Size of wordlist: {len(words)}")
print(f"Possible first guesses:  {most_common_letters(words, True)}")

while True:
    guess = input("Guess: ").lower()
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
