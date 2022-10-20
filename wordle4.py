from wordle_funcs import *
import colored
import sys
import time

def main():
    # Get the word list
    answer_list = get_answer_list()
    guess_list = get_guess_list()

    # Colors for printing
    green = colored.bg('green')
    yellow = colored.bg('yellow')
    black = colored.bg('black')
    reset = colored.attr('reset')

    hide_words = False
    try:
        if sys.argv[1] == "--hide-words":
            hide_words = True
            print("Hidden words mode is on!")
    except IndexError:
        pass

    # Print introduction
    print("Welcome to Wordle Solve 4.0!")
    try:
        with open('.suppress_changelog', 'r') as _:
            pass
    except FileNotFoundError:
        print("===Changes in 4.0")
        print(" * Allows correct WORDLE word to be entered")
        print(" * Colors are autofilled if correct WORDLE word was entered")
        print(" * Shows best next guesses if WORDLE word was entered")
        print(" * Shows mean, median, best, worst guesses compared to previous guess")
        print(" * Minor coloring changes")
        print("===Changes in 3.0")
        print(" * Fixed duplicate letters not being used in analysis")
        print(" * Uses more accurate word lists from wordle source")
        print(" * Remaining words display in a grid")
        print(" * Number of remaining words now color coded")

    # List of guesses that have been made
    guesses = []
    # List of colors that resulted from the guesses
    colors_list = []
    # Store yes/no user input
    check = ""

    '''
    4.1 IDEA:
    Tell the user what percentile their most recent guess was.
    This would require analyzing all guesses (maybe just WORDLE words for speed) and calculating.
    Also, try to optimize the algorithm to increase speed.

    4.0 UPDATES
    PROGRAM LOOP:
    1. Enter correct WORDLE word first

    ====
    2. Type in a guess
        - list how many words are left after that guess
        - list a breakdown of other guesses that would have been good also
        - list the percentile that your guess was out of possible guesses
    3. This can repeat with multiple guesses. No need to enter colors (the program already
       knows the colors because it knows the correct WORDLE word).
    ====
    '''

    # Get the correct WORDLE word
    correct_word = ""
    print()
    correct_word = input("Enter the correct WORDLE word here: ")
    while True:
        if correct_word == "":
            print("Proceeding with unknown WORDLE word...")
            break

        if len(correct_word) != 5:
            print(f"{colored.fg('red')}Error, {correct_word} is {len(correct_word)} letters long. Must be 5.{colored.attr('reset')}")
            correct_word = input("Try again: ")
            continue

        if correct_word not in answer_list:
            check = input(f"{colored.fg('red')}The word {correct_word} does not appear in the answer list. Enter 'yes' to override: {colored.attr('reset')}") 
            
            if check == 'yes':
                break
            else:
                correct_word = input("Try again: ")
                continue
        break

    #
    # Guess loop
    #
    print("\nWe'll start by having you write the guesses that you have done so far.")
    while True:
        # Fill in the guesses list while making sure the user enters valid input
        while True:
            word = input(f"{colored.fg('yellow')}Guess #{len(guesses)+1}: {colored.attr('reset')}")

            if word == "":
                break

            if len(word) != 5:
                print("Each guess must be five letters. Input not counted.")
                continue

            if word not in guess_list:
                check = input(f"That's likely not a valid WORDLE guess. Type '{colored.fg('green')}yes{colored.attr('reset')}' if you are sure you made this guess: ")
                
                if check != "yes":
                    continue

            guesses.append(word);
            if correct_word != "":
                colors_list.append(''.join(gen_colors(word, correct_word)))

        print("\nNice! Now we'll record the colors that resulted from those guesses.")

        # Fill in the colors list while making sure the user enters valid input
        # depecrated
        if correct_word == "":
            colors = ""
            while len(colors_list) != len(guesses):
                colors = input(f"Colors from guess #{len(colors_list)+1}: ")
                colors = colors.lower()

                if len(colors) != 5:
                    print("Sorry, all inputs must be five letters. Input not counted.")
                    continue

                correct = True
                for char in colors:
                    if char != "y" and char != "g" and char != "b":
                        print(f"Sorry, there is an invalid character. Input not counted.")
                        correct = False
                        break

                if not correct:
                    continue

                colors_list.append(colors)

        # Print the wordle guesses and colors
        print("\nAlright. Just to confirm, here's what you entered:")
        i = 0
        while i < len(guesses):
            for index, char in enumerate(guesses[i]):
                if colors_list[i][index] == 'b':
                    print(black + char + reset, end="")
                elif colors_list[i][index] == 'y':
                    print(yellow + char + reset, end="")
                elif colors_list[i][index] == 'g':
                    print(green + char + reset, end="")
            print()
            i += 1

        stime = time.time()
        narrowed_answers = []
        exp_search = ""
        for word in answer_list:
            if is_valid_colors(guesses, colors_list, word):
                narrowed_answers.append(word)

        if len(narrowed_answers) == 0:
            print("\nThere are no valid wordle answers for your guesses. Expanding search to all valid English five letter words...")
            for word in guess_list:
                if is_valid_colors(guesses, colors_list, word):
                    narrowed_answers.append(word)
            exp_search = colored.fg("magenta_2a") + colored.bg("tan") + "[EXPANDED SEARCH]" + colored.attr("reset") + " "

        if not hide_words:
            i = 0
            while i < len(narrowed_answers):
                if i % 9 == 0:
                    print()
                print(narrowed_answers[i], end="     ")
                i += 1

        app_char = ''
        verb = ''
        if len(narrowed_answers) == 1:
            app_char = ''
            verb = 'is'
        else:
            app_char = 's'
            verb = 'are'

        if len(narrowed_answers) > 100:
            print(colored.fg("red") + f"\n{exp_search}There {verb} {len(narrowed_answers)} word{app_char} left." + colored.attr("reset"))
        elif len(narrowed_answers) > 30:
            print(colored.fg("cyan") + f"\n{exp_search}There {verb} {len(narrowed_answers)} word{app_char} left." + colored.attr("reset"))
        elif len(narrowed_answers) > 10:
            print(colored.fg("yellow") + f"\n{exp_search}There {verb} {len(narrowed_answers)} word{app_char} left." + colored.attr("reset"))
        else:
            print(colored.fg("green") + f"\n{exp_search}There {verb} {len(narrowed_answers)} word{app_char} left." + colored.attr("reset"))

        if colors_list[-1] == 'ggggg':
            print(colored.fg("light_sea_green") + "\nCongrats, looks like you solved it!" + colored.attr("reset"))
            print(colored.fg("yellow") + "Good luck on your future WORDLEs." + colored.attr("reset"))
            break
        # analysis of guess
        if correct_word == "":
            print(colored.fg("yellow") + "Enter the correct WORDLE word for guess analysis" + colored.attr("reset"))
        elif hide_words == True:
            print("Guess analysis not shown in hide word mode.")
        else:
            print(colored.fg("sea_green_2") + "\n* Last Guess Analysis *" + colored.attr("reset"))

            last_guess = guesses.pop()
            last_colors = colors_list.pop()

            old_narrowed_answers = []
            for word in answer_list:
                if is_valid_colors(guesses, colors_list, word):
                    old_narrowed_answers.append(word)

            sorted_reasonable_guesses = []
            for index, guess in enumerate(old_narrowed_answers):
                display_prog(index, len(old_narrowed_answers))

                sorted_reasonable_guesses.append((guess, get_words_remaining(guesses, colors_list, guess, correct_word, answer_list)))
            wipe_prog()

            sorted_reasonable_guesses.sort(key=lambda x: x[1])

            total = 0
            for elem in sorted_reasonable_guesses:
                total += elem[1]

            avg = total / len(sorted_reasonable_guesses)
            median = sorted_reasonable_guesses[round(len(sorted_reasonable_guesses)/2)]
            your_guess = len(narrowed_answers)

            guesses.append(last_guess)
            colors_list.append(last_colors)

            if len(old_narrowed_answers) > 1:
                print(f" - There were {len(old_narrowed_answers)} guesses to choose from.")
            else:
                print(f" - There was {len(old_narrowed_answers)} guess to choose from.")

            print(f"\n - You guessed {colored.fg('sky_blue_2')}{last_guess}{colored.attr('reset')} and \
ended up with {colored.fg('sky_blue_2')}{len(narrowed_answers)}{colored.attr('reset')} word(s) left.")
            print(f" - The median guess was {colored.fg('sky_blue_2')}{median[0]}{colored.attr('reset')} which \
ended up with {colored.fg('sky_blue_2')}{median[1]}{colored.attr('reset')} word(s) left.")
            print(f" - The average guess ended up with {colored.fg('sky_blue_2')}{avg:.2f}{colored.attr('reset')} word(s) left.")

            print(f"\n - The best guess was {colored.fg('sky_blue_2')}{sorted_reasonable_guesses[0][0]}{colored.attr('reset')} which \
ended up with {colored.fg('sky_blue_2')}{sorted_reasonable_guesses[0][1]}{colored.attr('reset')} word(s) left.")
            print(f" - The worst guess was {colored.fg('sky_blue_2')}{sorted_reasonable_guesses[-1][0]}{colored.attr('reset')} which \
ended up with {colored.fg('sky_blue_2')}{sorted_reasonable_guesses[-1][1]}{colored.attr('reset')} word(s) left.")

            print(colored.fg("sea_green_2") + "\n* Best Next Guesses *" + colored.attr("reset"))

            sorted_reasonable_guesses = []
            for index, guess in enumerate(narrowed_answers):
                display_prog(index, len(narrowed_answers))

                sorted_reasonable_guesses.append((guess, get_words_remaining(guesses, colors_list, guess, correct_word, answer_list)))
            wipe_prog()

            sorted_reasonable_guesses.sort(key=lambda x: x[1])
            narrowed_guesses = [elem for index, elem in enumerate(sorted_reasonable_guesses) if sorted_reasonable_guesses[index][1] == 1 or index < 5]
            
            num_worst = min(3, len(sorted_reasonable_guesses))
            worst_guesses = [elem for elem in sorted_reasonable_guesses[num_worst*-1:] if elem not in narrowed_guesses]

            median_guess = sorted_reasonable_guesses[round(len(sorted_reasonable_guesses)/2)]
            median_guess_ind = sorted_reasonable_guesses.index(median_guess)

            for i, elem in enumerate(narrowed_guesses):
                if len(str(len(narrowed_guesses))) == 2:
                    print(f"{colored.fg('yellow')}{i+1:2}{colored.attr('reset')} {colored.fg('purple_1a')}->\
{colored.attr('reset')} {colored.fg('sky_blue_2')}{elem[0]}{colored.attr('reset')} (Narrows to {elem[1]})")
                elif len(str(len(narrowed_guesses))) == 3:
                    print(f"{colored.fg('yellow')}{i+1:3}{colored.attr('reset')} {colored.fg('purple_1a')}->\
{colored.attr('reset')} {colored.fg('sky_blue_2')}{elem[0]}{colored.attr('reset')} (Narrows to {elem[1]})")
                else:
                    print(f"{colored.fg('yellow')}{i+1}{colored.attr('reset')} {colored.fg('purple_1a')}->\
{colored.attr('reset')} {colored.fg('sky_blue_2')}{elem[0]}{colored.attr('reset')} (Narrows to {elem[1]})")

            if median_guess not in narrowed_guesses and median_guess not in worst_guesses:
                print()
                print(f"{colored.fg('yellow')}{median_guess_ind+1}{colored.attr('reset')} {colored.fg('purple_1a')}->\
{colored.attr('reset')} {colored.fg('sky_blue_2')}{median_guess[0]}{colored.attr('reset')} (Narrows to {median_guess[1]})")

            if len(worst_guesses) != 0:
                print()
            else:
                print("\n(end of list)")
            
            for elem in worst_guesses:
                print(f"{colored.fg('yellow')}{sorted_reasonable_guesses.index(elem)+1}{colored.attr('reset')} {colored.fg('purple_1a')}->\
{colored.attr('reset')} {colored.fg('sky_blue_2')}{elem[0]}{colored.attr('reset')} (Narrows to {elem[1]})")


        print("\nEnter your next guess if you would like...")

if __name__ == "__main__":
    main()
