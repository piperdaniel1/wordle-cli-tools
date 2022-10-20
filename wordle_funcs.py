import colored

def get_words():
    with open('words.txt', 'r') as f:
        words = f.readlines()

    return [word.replace("\n", "") for word in words]

def get_guess_list():
    with open('all_guesses.txt', 'r') as f:
        guesses = f.readlines()

    return [guess.replace("\n", "") for guess in guesses]

def get_answer_list():
    with open('answer_list.txt', 'r') as f:
        answers = f.readlines()

    return [answer.replace("\n", "") for answer in answers]

# this is probably bad, but the WORDLE bot uses this code to 
# generate a score for a guess. Maybe this should be in a different
# file, but fuck it.
# scale is the number of points that the best letter will be worth
def get_letter_frequencies(scale = 100):
    answer_list = get_answer_list()

    letters = {}
    for answer in answer_list:
        for letter in answer:
            if letter in letters:
                letters[letter] += 1/len(answer_list)
            else:
                letters[letter] = 1/len(answer_list)

    letters_sorted = sorted(letters.items(), key=lambda x: x[1], reverse=True)

    letter_map = {}
    for elem in letters_sorted:
        letter_map[elem[0]] = round(elem[1] * (scale / letters_sorted[0][1]), 1)

    return letter_map

def get_letter_pos_freq(scale = 100):
    answer_list = get_answer_list()

    letter_positions = [{} for _ in range(5)]
    
    index = 0
    while index < len(letter_positions):
        for answer in answer_list:
            letter = answer[index]
            if letter in letter_positions[index]:
                letter_positions[index][letter] += 1/len(answer_list)
            else:
                letter_positions[index][letter] = 1/len(answer_list)
        index += 1

    index = 0
    letters_sorted = []
    while index < len(letter_positions):
        letters_sorted.append(sorted(letter_positions[index].items(), key=lambda x: x[1], reverse=True))
        index += 1

    letters_map = []
    index = 0
    while index < len(letters_sorted):
        letter_map = {}
        for elem in letters_sorted[index]:
            letter_map[elem[0]] = round(elem[1] * (scale / letters_sorted[index][0][1]), 1)
        letters_map.append(letter_map)
        index += 1

    return letters_map

# Code to display a progress bar in this format
# [===========       ]
# curr and total can be any numbers, as long as curr counts up to total and the task finishes
# when it reaches it
def display_prog(curr, total, bars=100, barchar='=', emptychar=' ', border_left='[', border_right=']'):
    num_bars = round((float(curr) / float(total)) * bars)

    prog = float(curr) / float(total)
    if prog < 0.3:
        print(colored.fg("red"), end="")
    elif prog < 0.75:
        print(colored.fg("yellow"), end="")
    else:
        print(colored.fg("green"), end="")

    print(border_left + (barchar * num_bars) + (emptychar * (bars - num_bars)) + \
            border_right, end="\r") 
    print(colored.attr("reset"), end="")
def wipe_prog(bars=100):
    print(' ' * (bars+2), end="\r")

def get_num_letters(word, letter):
    num = 0
    for char in word:
        if char == letter:
            num += 1
    return num

def get_num_chars(char, string):
    num = 0
    for elem in string:
        if char == elem:
            num += 1
    return num

def num_detracting_chars(char, guess, colors_list):
    num = 0
    for i, elem in enumerate(guess):
        if char == elem:
            if colors_list[i] == 'g' or colors_list[i] == 'y':
                num += 1
    return num

def gen_colors(guess, answer):
    colors_list = ['' for _ in range(len(guess))]
    cache = {}
    for i, char in enumerate(guess):
        if char == answer[i]:
            colors_list[i] = 'g'
            if char not in cache:
                cache[char] = 1
            else:
                cache[char] += 1
        elif char not in answer:
            colors_list[i] = 'b'

    for i, char in enumerate(guess):
        if char == answer[i] or char not in answer:
            continue

        # important things:
        # a: NUM OF char IN ANSWER
        a = get_num_chars(char, answer)
        # b: NUM OF char IN GUESS THAT ARE GREEN
        # c: NUM OF char IN GUESS THAT ARE YELLOW
        # b = b+c
        # b = num_detracting_chars(char, guess, colors_list)

        if char in cache:
            b = cache[char]
        else:
            b = 0

        # a-b-c= d: NUM THAT CAN BE STILL COLORED YELLOW IN GUESS
        # if d > 0 then COLOR YELLOW
        # chars are colored yellow from left to right
        if a-b > 0:
            colors_list[i] = 'y'

            if char not in cache:
                cache[char] = 1
            else:
                cache[char] += 1
        else:
            colors_list[i] = 'b'

    return colors_list

# Checks if the colors_list is valid
# Returns True if it is, False if it isn't
# Used to use gen_colors() but switched to integrate gen_colors code into
# this because we only need a True/False value.
# This is harder to understand, but it's more efficient
def is_valid_colors(guesses, correct_colors_list, answer):
    for i, guess in enumerate(guesses):
        cache = {}
        for j, char in enumerate(guess):
            if char == answer[j]:
                if correct_colors_list[i][j] != 'g':
                    return False

                if char not in cache:
                    cache[char] = 1
                else:
                    cache[char] += 1
            elif char not in answer:
                if correct_colors_list[i][j] != 'b':
                    return False

        for j, char in enumerate(guess):
            if char == answer[j] or char not in answer:
                continue

            # important things:
            # a: NUM OF char IN ANSWER
            a = get_num_chars(char, answer)
            # b: NUM OF char IN GUESS THAT ARE GREEN
            # c: NUM OF char IN GUESS THAT ARE YELLOW
            # b = b+c
            # b = num_detracting_chars(char, guess, colors_list)

            if char in cache:
                b = cache[char]
            else:
                b = 0

            # a-b-c= d: NUM THAT CAN BE STILL COLORED YELLOW IN GUESS
            # if d > 0 then COLOR YELLOW
            # chars are colored yellow from left to right
            if a-b > 0:
                if correct_colors_list[i][j] != 'y':
                    return False

                if char not in cache:
                    cache[char] = 1
                else:
                    cache[char] += 1
            else:
                if correct_colors_list[i][j] != 'b':
                    return False

    return True

def get_words_remaining(guesses, colors_list, new_guess, correct_word, full_ans_list):
    new_color = gen_colors(new_guess, correct_word)

    guesses.append(new_guess)
    colors_list.append(new_color)

    num_rem = 0
    for word in full_ans_list:
        if is_valid_colors(guesses, colors_list, word):
            num_rem += 1

    guesses.pop()
    colors_list.pop()

    return num_rem
