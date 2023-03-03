import random


def load(num=int):

    if num == 5:
        possible_words = open(
            "wordle_bot_tester/possible_words.txt", "r").read().splitlines()
    else:
        possible_words = open("wordle/words_alpha.txt", "r").read().splitlines()
        possible_words = [s for s in possible_words if len(s) == num]
    
    global word
    word = random.choice(possible_words)


def eval_attempt(guess, num=int):
    result_list = [' '] * num
    word_list = list(word)
    guess_list = list(guess)

    for index, char in enumerate(guess):
        if char == word[index]:
            result_list[index] = 'g'
            guess_list[index] = '0'
            word_list.remove(char)

    for index, char in enumerate(guess_list):
        if char != '0':
            if char in word_list:
                result_list[index] = 'y'
                guess_list[index] = '0'
                word_list.remove(char)
            else:
                result_list[index] = 'w'
    result = ""
    for char in result_list:
        result += char

    return result
