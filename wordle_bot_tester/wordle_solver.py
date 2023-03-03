import wordle_puzzle

iterations = 100
number_of_letters = 7
wins = 0
losses = 0
correct_words = []
incorrect_words = []
number_of_guesses = []


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

        for i in range(number_of_letters):
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


def main(iterations):
    global wins
    global losses
    global correct_words
    global incorrect_words
    global number_of_guesses

    for _ in range(iterations):
        if number_of_letters == 5:
            words = open("wordle/words.txt", "r").read().splitlines()
            wordle_puzzle.load(5)
        else:
            words = open("wordle/words_alpha.txt", "r").read().splitlines()
            words = [s for s in words if len(s) == number_of_letters]
            wordle_puzzle.load(number_of_letters)

        for i in range(1, 7):

            guess = most_common_letters(words, True)
            if len(guess) == 0:
                guess = most_common_letters(words, False)

            guess = guess[0]

            result = wordle_puzzle.eval_attempt(guess, number_of_letters)
            if result == "g" * number_of_letters:
                wins += 1
                correct_words.append(guess)
                number_of_guesses.append(i)
                break

            words = filter_word_list(words, guess, result)
        else:
            incorrect_words.append(wordle_puzzle.word)
            losses += 1
            number_of_guesses.append(i)

    else:
        print("Total wins: ", wins)
        print("Total losses: ", losses)
        print("Win rate: ", (wins / (wins + losses)) * 100)
        print()
        print("Correct words: ", correct_words)
        print()
        print("Incorrect words: ", incorrect_words)
        print()
        print("Average number of guesses: {0}".format(
            sum(number_of_guesses) / len(number_of_guesses)))


main(iterations)
