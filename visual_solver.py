from words import get_words
import colored

words = get_words()
green = colored.bg('green')
yellow = colored.bg('yellow')
black = colored.bg('black')
reset = colored.attr('reset')

print("Welcome to the Wordle Solve 2.0!")
print("Wordle Solve 2.0 is great for when Wordle Solve 1.0 does not give you precise enough answers.")
print("It's also just a better Wordle Solver in general.")
print("Known issues: ")
print(" * Ignores cases where there are clues based on duplicate letters in words")

print("\nWe'll start by having you write the guesses that you have done so far.")

guesses = []
colors_list = []
check = ""

while True:
    print("\nEnter your next guess if you would like...")
    while True:
        word = input(f"Guess #{len(guesses)+1}: ")

        if word == "":
            break

        if len(word) != 5:
            print("Each guess must be five letters. Input not counted.")
            continue

        if word not in words:
            check = input("That's likely not a valid WORDLE guess. Type 'yes' if you are sure you made this guess: ")
            
            if check != "yes":
                continue

        guesses.append(word);

    print("\nNice! Now we'll record the colors that resulted from those guesses.")

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

    #
    # Solver part of code
    #

    # Gets rid of any words that don't fit the green characters
    i = len(words) - 1
    while i >= 0:
        for j, letter in enumerate(green_letters):
            if words[i][j] != letter and letter != "_":
                words.pop(i)
                break

        i -= 1

    # Gets rid of any words that don't fit the grey characters
    i = len(words) - 1
    while i >= 0:
        for letter in words[i]:
            if letter in banned_letters and letter not in green_letters and letter not in yellow_letters:
                words.pop(i)
                break

        i -= 1

    # Gets rid of any words that have matching yellow character slots (banned_slots)
    i = len(words) - 1
    while i >= 0:
        for j, letter in enumerate(words[i]):
            if letter in banned_slots[j]:
                words.pop(i)
                break

        i -= 1

    # Gets rid of any words that are missing yellow characters
    i = len(words) - 1
    while i >= 0:
        for j, letter in enumerate(yellow_letters):
            if letter not in words[i]:
                words.pop(i)
                break

        i -= 1

    print(words)
    print(f"There are {len(words)} total words.")
