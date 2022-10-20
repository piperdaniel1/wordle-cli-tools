from wordle_funcs import *
import colored
import time
from typing import Dict, List
import os
import sys

def score_word(word : str, score_map : Dict[str, int]) -> int:
    score = 0

    for index, letter in enumerate(word):
        if word.index(letter) == index:
            score += score_map[letter]
        else:
            score -= 20

    return score

def score_word_pos(word : str, score_map : List[Dict[str, int]]) -> int:
    score = 0

    for index, letter in enumerate(word):
        if word.index(letter) == index:
            try:
                score += score_map[index][letter]
            except KeyError:
                score += 0
        else:
            score -= 20

    return score

def get_full_average():
    score_map = get_letter_frequencies()
    answers = get_answer_list()
    round_log = []
    fails_list = []
    two_guesses = []
    fails = 0

    for cindex, correct_word in enumerate(answers):
        os.system('clear')
        print(correct_word, "-", cindex)
        guess_list = []
        color_list = []
        words_remaining = answers[:]

        while True:
            best_word = ""
            best_score = 0
            for word in words_remaining:
                score = score_word(word, score_map)
                if score > best_score:
                    best_word = word
                    best_score = score

            guess_list.append(best_word)
            color_list.append(gen_colors(best_word, correct_word))

            if best_word == correct_word or len(guess_list) == 6:
                break

            index = len(words_remaining) - 1
            while index >= 0:
                if not is_valid_colors(guess_list, color_list, words_remaining[index]):
                    words_remaining.pop(index)
                index -= 1

        if len(guess_list) == 2:
            two_guesses.append(correct_word)
        if guess_list[-1] != correct_word:
            fails += 1
            fails_list.append(correct_word)

        else:
            round_log.append(len(guess_list))

    try:
        print(f"Average: {sum(round_log) / len(round_log)}")
    except ZeroDivisionError:
        print("There were no successful rounds.")

    print(f"Fails: {fails}")
    print(fails_list)
    print("Two guesses:")
    print(two_guesses)

def display_guess_preview(guess):
    print("-" * 67)
    print("|" + " " * 65 + "|")
    print("|" + " " * 30 + str(guess) + " " * 30 + "|") 
    print("|" + " " * 65 + "|")
    print("-" * 67)

def main():
    try:
        if sys.argv[1] == "--calc-avg":
            get_full_average()
            return
    except IndexError:
        pass

    score_map = get_letter_pos_freq()

    # Get the word list
    answer_list = get_answer_list()
    guess_list = get_guess_list()

    # Colors for printing
    green = colored.bg('green')
    yellow = colored.bg('yellow')
    black = colored.bg('black')
    reset = colored.attr('reset')

    # Print introduction
    print("Welcome to Wordle Bot 1.0!")
    try:
        with open('.suppress_changelog', 'r') as _:
            pass
    except FileNotFoundError:
        print("===Changes in 1.0")
        print("------ Basic bot ------")

    # Get the correct WORDLE word
    print()
    correct_word = input("Enter the correct WORDLE word here (don't worry I won't cheat :) ): ")

    while True:
        if correct_word not in answer_list:
            print("Hey, the word you entered is not in the answer list! Try again: ", end="")
            correct_word = input()
        else:
            break

    guess_list = []
    color_list = []
    words_remaining = answer_list[:]

    best_word = ""
    best_score = 0

    # Get the best guess
    for word in words_remaining:
        score = score_word_pos(word, score_map)
        if score > best_score:
            best_word = word
            best_score = score

    # guess loop
    os.system('clear')
    while True:
        #
        # DISPLAY THE GUESS
        #
        print("==================================================================")
        print("        |                                                |        ")
        print(f"        |                 {colored.fg('green')}Guess Number {len(guess_list) + 1}{colored.attr('reset')}                 |        ")
        print("        |                                                |        ")
        print("==================================================================")

        print()
        print(" " * 18 + f"I have decided to guess {colored.fg('yellow')}{best_word}{colored.attr('reset')}!" + " " * 18)
        print()

        time.sleep(0.02)
        for _ in range(66):
            print(".", end="", flush=True)
            time.sleep(0.02)
        print("                     ", end="")
        print("\n")
    
        print(" " * 22 + "The colors were: ", end="")
        
        colors = gen_colors(best_word, correct_word)

        for index, color in enumerate(colors):
            if color == 'g':
                print(f"{green}{best_word[index]}{reset}", end="")
            elif color == 'y':
                print(f"{yellow}{best_word[index]}{reset}", end="")
            elif color == 'b':
                print(f"{black}{best_word[index]}{reset}", end="")

        print("\n")

        if best_word != correct_word:
            time.sleep(5)
        else:
            time.sleep(3)

        guess_list.append(best_word)
        color_list.append(colors)

        if best_word == correct_word:
            print(" " * 27 + "Yay, I won!" + " " * 27)
            break

        if len(guess_list) == 6:
            print(" " * 18 + "Dang, that's all my guesses." + " " * 18)
            break

        best_word = ""
        best_score = 0

        # Get the best guess
        for word in words_remaining:
            score = score_word_pos(word, score_map)
            if score > best_score:
                best_word = word
                best_score = score

        #
        # GUESS SELECTION ANIMATION
        # 
        index = len(words_remaining) - 1
        while index >= 0:
            if not is_valid_colors(guess_list, color_list, words_remaining[index]):
                words_remaining.pop(index)

            index -= 1

        best_word = ""
        best_score = 0

        # Get the best guess
        for word in words_remaining:
            score = score_word_pos(word, score_map)
            if score > best_score:
                best_word = word
                best_score = score

        for word in words_remaining:
            if word == best_word:
                continue
            os.system('clear')
            print()
            print(" " * 21 + f"{colored.fg('yellow')}Coming up with a guess...{colored.attr('reset')}" + " " * 21)
            print()
            display_guess_preview(word)
            time.sleep(min(5 / len(words_remaining), 0.5))

        os.system('clear')
        print()
        print(" " * 21 + f"{colored.fg('yellow')}Coming up with a guess...{colored.attr('reset')}" + " " * 21)
        print()
        display_guess_preview(best_word)
        time.sleep(1)

        print()
        print("Alright, I have my guess!")
        time.sleep(2)

        os.system('clear')

    print("\n" * 2)
    print(" " * 23 + f"{colored.fg('yellow')}Final Guess Breakdown{colored.attr('reset')}" + " " * 23)
    print()
    for index, guess in enumerate(guess_list):
        print(" " * 31, end="")
        for char_index, char in enumerate(guess):
            if color_list[index][char_index] == 'g':
                print(f"{green}{char}{reset}", end="")
            elif color_list[index][char_index] == 'y':
                print(f"{yellow}{char}{reset}", end="")
            elif color_list[index][char_index] == 'b':
                print(f"{black}{char}{reset}", end="")
        print()

    print()
    if best_word == correct_word:
        if len(guess_list) <= 3:
            print(" " * 18 + f"{colored.fg('green')}I got the word in {len(guess_list)} guesses! :){colored.attr('reset')}")
        elif len(guess_list) == 4:
            print(" " * 18 + f"{colored.fg('white')}I got the word in {len(guess_list)} guesses! :){colored.attr('reset')}")
        elif len(guess_list) > 4:
            print(" " * 18 + f"{colored.fg('yellow')}I got the word in {len(guess_list)} guesses.{colored.attr('reset')}")
    else:
        print(" " * 20 + f"{colored.fg('red')}I couldn't find the word :({colored.attr('reset')}")
    print("\n" * 10)

 
if __name__ == "__main__":
    main()
