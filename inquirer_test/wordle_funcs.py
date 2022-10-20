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
    for i, char in enumerate(guess):
        if char == answer[i]:
            colors_list[i] = 'g'
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
        b = num_detracting_chars(char, guess, colors_list)
        # a-b-c= d: NUM THAT CAN BE STILL COLORED YELLOW IN GUESS
        # if d > 0 then COLOR YELLOW
        # chars are colored yellow from left to right
        if a-b > 0:
            colors_list[i] = 'y'
        else:
            colors_list[i] = 'b'

    return colors_list

# Checks if the colors_list is valid
# Returns True if it is, False if it isn't
def is_valid_colors(guesses, colors_list, word):
    for i, guess in enumerate(guesses):
        colors = gen_colors(guess, word)
        for j, char in enumerate(colors):
            if char != colors_list[i][j]:
                return False

    return True

def get_words_remaining(guesses, colors_list, new_guess, correct_word, full_ans_list):
    new_color = gen_colors(new_guess, correct_word)

    new_guesses = guesses[:]
    new_colors_list = colors_list[:]
    new_guesses.append(new_guess)
    new_colors_list.append(new_color)

    narrowed_answers = []
    for word in full_ans_list:
        if is_valid_colors(new_guesses, new_colors_list, word):
            narrowed_answers.append(word)

    return len(narrowed_answers)
