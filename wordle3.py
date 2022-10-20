from words import get_answer_list, get_guess_list
import colored

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

#deprecated
def narrow_list(guesses,colors_list, answer_list):
    # Populate green, yellow, and banned letter lists for solver
    green_letters = ["_", "_", "_", "_", "_"] 
    for i, guess in enumerate(guesses):
        for j, char in enumerate(guess):
            if colors_list[i][j] == 'g':
                green_letters[j] = char
    yellow_letters = []
    banned_slots = [[], [], [], [], []]
    for i, guess in enumerate(guesses):
        for j, char in enumerate(guess):
            if colors_list[i][j] == 'y':
                yellow_letters.append(char)
                banned_slots[j].append(char)
    banned_letters = []
    for i, guess in enumerate(guesses):
        for j, char in enumerate(guess):
            if colors_list[i][j] == 'b':
                banned_letters.append(char)

    # Minimum letter count in final word for each letter
    letter_counts = [0 for _ in range(26)]
    for i, guess in enumerate(guesses):
        # format: [[letter, [index, index, index]], [letter, [index, index]], ...]
        duplicate_letters = []
        for j, char in enumerate(guess):
            index_list = []
            for k, char2 in enumerate(guess):
                if char2 == char:
                    index_list.append(k)

            if len(index_list) > 1:
                duplicate_letters.append([char, index_list])

        for letter in duplicate_letters:
            char = letter[0]
            ind_list = letter[1]

            for count, ind in enumerate(ind_list):
                if colors_list[i][ind] == 'b':
                    if letter_counts[ord(char) - ord('a')] < count:
                        letter_counts[ord(char) - ord('a')] = count
                        break

                if count == len(ind_list) - 1:
                    if letter_counts[ord(char) - ord('a')] < count+1:
                        letter_counts[ord(char) - ord('a')] = count+1

    #
    # Solver part of code
    #

    # Gets rid of any words that don't fit the green characters
    i = len(answer_list) - 1
    while i >= 0:
        for j, letter in enumerate(green_letters):
            if answer_list[i][j] != letter and letter != "_":
                answer_list.pop(i)
                break
        i -= 1

    # Gets rid of any words that contain the grey characters
    i = len(answer_list) - 1
    while i >= 0:
        for letter in answer_list[i]:
            if letter in banned_letters and letter not in green_letters and letter not in yellow_letters:
                answer_list.pop(i)
                break
        i -= 1

    # Gets rid of any words that have a yellow letter in the same place as the same yellow letter was found
    # Example: "dodge" is the goal word
    #          "adjar" is the first guess
    #          the d is colored yellow
    # This allows words like "idles" to be removed because it has a yellow letter in the same place as the yellow letter in "adjar"
    # If "idles" was the word, the d would have been green when we guessed "adjar"
    i = len(answer_list) - 1
    while i >= 0:
        for j, letter in enumerate(answer_list[i]):
            if letter in banned_slots[j]:
                answer_list.pop(i)
                break
        i -= 1

    # Gets rid of any words that are missing yellow characters
    i = len(answer_list) - 1
    while i >= 0:
        for j, letter in enumerate(yellow_letters):
            if letter not in answer_list[i]:
                answer_list.pop(i)
                break
        i -= 1

    # Gets rid of any words that have a letter that appears too few times
    i = len(answer_list) - 1
    while i >= 0:
        for j, letter in enumerate(answer_list[i]):
            if get_num_letters(answer_list[i], letter) < letter_counts[ord(letter) - ord('a')]:
                if answer_list[i] == "primo":
                    print("popped primo because: " + str(get_num_letters(answer_list[i], letter)) + " < " + str(letter_counts[ord(letter) - ord('a')]))
                answer_list.pop(i)
                break
        i -= 1

    return answer_list


# Get the word list
answer_list = get_answer_list()
guess_list = get_guess_list()

# Colors for printing
green = colored.bg('green')
yellow = colored.bg('yellow')
black = colored.bg('black')
reset = colored.attr('reset')

# Print introduction
print("Welcome to the Wordle Solve 3.0!")
try:
    with open('.suppress_changelog', 'r') as f:
        pass
except FileNotFoundError:
    print("Changes since 2.0:")
    print(" * Fixed duplicate letters not being used in analysis")
    print(" * Uses more accurate word lists from wordle source")
    print(" * Remaining words display in a grid")
    print(" * Number of remaining words now color coded")

#print("Known issues: ")
#print(" * Ignores cases where there are clues based on duplicate letters in words")

# List of guesses that have been made
guesses = []
# List of colors that resulted from the guesses
colors_list = []
# Store yes/no user input
check = ""

#
# Guess loop
#
print("\nWe'll start by having you write the guesses that you have done so far.")
while True:
    # Fill in the guesses list while making sure the user enters valid input
    while True:
        word = input(f"Guess #{len(guesses)+1}: ")

        if word == "":
            break

        if len(word) != 5:
            print("Each guess must be five letters. Input not counted.")
            continue

        if word not in guess_list:
            check = input("That's likely not a valid WORDLE guess. Type 'yes' if you are sure you made this guess: ")
            
            if check != "yes":
                continue

        guesses.append(word);

    print("\nNice! Now we'll record the colors that resulted from those guesses.")

    # Fill in the colors list while making sure the user enters valid input
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
    '''
    narrowed_answers = narrow_list(guesses, colors_list, answer_list[:])
    exp_search = ""
    if len(narrowed_answers) == 0:
        print("\nThere are no valid wordle answers for your guesses. Expanding search to all valid English five letter words...")
        narrowed_answers = narrow_list(guesses, colors_list, guess_list[:])
        exp_search = colored.fg("magenta_2a") + colored.bg("tan") + "[EXPANDED SEARCH]" + colored.attr("reset") + " "
    ''' 
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

    narrowed_answers.sort()

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

    print("\nEnter your next guess if you would like...")

