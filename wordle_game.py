from wordle_funcs import *
import inquirer
from inquirer.themes import WordleTheme
import colored
import os
import time

class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.guess_list = []
        self.completed = False
    
    def get_guesses_left(self):
        return 6 - len(self.guess_list)

def get_next_guess(players, turn) -> int:
    print(f"{colored.fg('red')} * {colored.attr('reset')}State of the game:")
    print(f"{players[turn].name} picked the {colored.fg('green')}WORDLE{colored.attr('reset')} word.")

    print(f"\n{colored.fg('red')} * {colored.attr('reset')}Guesses left:")
    for index, player in enumerate(players):
        if index != turn:
            if player.completed:
                print(f"{player.name} found {players[turn].name}'s {colored.fg('green')}WORDLE{colored.attr('reset')} word in {len(player.guess_list)} guesses.")
            else:
                print(f"{player.name} has {colored.fg('cyan')}{6 - len(player.guess_list)}{colored.attr('reset')} guesses left.")

    print()
    list_choices = [player.name for player in players if player.name != players[turn].name and player.get_guesses_left() > 0 and player.completed == False]
    
    for index, player in enumerate(players):
        if len(player.guess_list) > 0:
            list_choices.append("Edit Previous Guesses")
            break

    list_choices.append("Add a player")

    if len(players) > 1:
        list_choices.append("Delete a player")
        list_choices.append("Reorder players")

    questions = [
        inquirer.List(
            "player",
            message=f"Select player to guess",
            choices=list_choices,
        ),
    ]

    answer = inquirer.prompt(questions, theme=WordleTheme()) # type: ignore
    for index, player in enumerate(players):
        if player.name == answer["player"]: # type: ignore
            return index

    if answer["player"] == "Edit Previous Guesses": # type: ignore
        return -2
    if answer["player"] == "Add a player": # type: ignore
        return -3
    if answer["player"] == "Delete a player": # type: ignore
        return -4
    if answer["player"] == "Reorder players": # type: ignore
        return -5

    return -1

def get_color_str(color):
    colors = {"g": "green", "y": "yellow", "b": "black"}

    if color in colors:
        return colors[color]
    else:
        return ""

def get_full_color_str(colors):
    color_str = ""
    for index, color in enumerate(colors):
        exp_color = get_color_str(color)
        colored_color = exp_color if exp_color != "black" else "light_slate_grey"

        color_str += colored.fg(colored_color) + get_color_str(color).upper() + colored.attr("reset")
        if index < len(colors) - 2:
            color_str += ", "
        elif index == len(colors) - 2:
            color_str += " and "

    return color_str

def edit_player(players, index):
    os.system("clear")
    print(f"{colored.fg('red')}Editing{colored.attr('reset')} {colored.fg('yellow')}{players[index].name}'s{colored.attr('reset')} {colored.fg('red')}guesses:{colored.attr('reset')}")
    list_choices = players[index].guess_list[:]
    list_choices.append(f"Go Back")

    print()
    questions = [
        inquirer.List(
            "guess",
            message="Choose a guess to remove",
            choices=list_choices,
        ),
    ]
    answer = inquirer.prompt(questions, theme=WordleTheme()) # type: ignore

    if answer["guess"] == "Go Back": # type: ignore
        return

    guess_index = players[index].guess_list.index(answer["guess"]) # type: ignore
    players[index].guess_list.pop(guess_index)

    if guess_index == len(players[index].guess_list):
        players[index].completed = False

def edit_prev_guesses(players, turn) -> int:
    os.system("clear")
    print(f"{colored.fg('red')}EDIT MODE:{colored.attr('reset')}")

    print()
    list_choices = [player.name for player in players if player.name != players[turn].name and len(player.guess_list) > 0]
    list_choices.append(f"Go Back")

    questions = [
        inquirer.List(
            "player",
            message="Choose a player to edit",
            choices=list_choices,
        ),
    ]

    answer = inquirer.prompt(questions, theme=WordleTheme()) # type: ignore
    for index, player in enumerate(players):
        if player.name == answer["player"]: # type: ignore
            return index

    if answer["player"] == "Go Back": # type: ignore
        return -2

    return -1

def choose_player_to_delete(players):
    os.system("clear")
    print(f"{colored.fg('red')}DELETE MODE:{colored.attr('reset')}")
    print("Careful... deleting a player can have unintended consequences.")

    print()
    list_choices = [player.name for player in players]
    list_choices.append(f"Go Back")

    questions = [
        inquirer.List(
            "player",
            message="Choose a player to delete",
            choices=list_choices,
        ),
    ]

    answer = inquirer.prompt(questions, theme=WordleTheme()) # type: ignore

    if answer["player"] == "Go Back": # type: ignore
        return -1

    for index, player in enumerate(players):
        if player.name == answer["player"]: # type: ignore
            players.pop(index)
            return index

    return -1

def add_player(players):
    os.system("clear")
    print(f"{colored.fg('red')}ADD MODE:{colored.attr('reset')}")

    print()
    questions = [
        inquirer.Text(
            "name",
            message="Enter the name of the player or nothing to cancel.",
        ),
    ]

    answer = inquirer.prompt(questions, theme=WordleTheme()) # type: ignore
    players.append(Player(answer["name"])) # type: ignore

def reorder_players(players):
    os.system("clear")
    print(f"{colored.fg('red')}REORDER MODE:{colored.attr('reset')}")

    print()
    list_choices = [player.name for player in players]
    list_choices.append(f"Go Back")

    questions = [
        inquirer.List(
            "player",
            message="Choose the first player to swap",
            choices=list_choices,
        ),
    ]


    index_swap1 = -1
    answer = inquirer.prompt(questions, theme=WordleTheme()) # type: ignore

    if answer["player"] == "Go Back": # type: ignore
        return
    for index, player in enumerate(players):
        if player.name == answer["player"]: # type: ignore
            index_swap1 = index
            break

    list_choices = [player.name for player in players if player.name != players[index_swap1].name]
    list_choices.append(f"Cancel Operation")

    questions = [
        inquirer.List(
            "player",
            message="Choose the second player to swap",
            choices=list_choices,
        ),
    ]


    index_swap2 = -1
    answer = inquirer.prompt(questions, theme=WordleTheme()) # type: ignore

    if answer["player"] == "Cancel Operation": # type: ignore
        return
    for index, player in enumerate(players):
        if player.name == answer["player"]: # type: ignore
            index_swap2 = index
            break

    players[index_swap1], players[index_swap2] = players[index_swap2], players[index_swap1]

# Get the word list
answer_list = get_answer_list()
guess_list = get_guess_list()

# Colors for printing
green = colored.bg('green')
yellow = colored.bg('yellow')
black = colored.bg('black')
reset = colored.attr('reset')

# Print introduction
print(f"Welcome to {colored.fg('green')}WORDLE Game 1.0{colored.attr('reset')}!")
try:
    with open('.suppress_changelog', 'r') as f:
        pass
except FileNotFoundError:
    print(" ** initial release **")

# List of guesses that have been made
guesses = []
# List of colors that resulted from the guesses
colors_list = []
# Store yes/no user input
check = ""

STRICT_MODE = True

players = []
while True:
    try:
        num_players = int(input(f"How many players? {colored.fg('cyan')}"))
        print(colored.attr('reset'), end="")
        break
    except ValueError:
        print("Please enter a number.")
        num_players = int(input("How many players? "))

for i in range(num_players):
    players.append(Player(input(f"Player " + str(i+1) + f" name: {colored.fg('yellow')}")))
    print(colored.attr('reset'), end="")

turn = 0
# main game loop
while True:
    os.system('clear')
    print(f"Alright {colored.fg('yellow')}{players[turn].name}{colored.attr('reset')}, it's your turn to pick a word!")
    
    # allow players[turn] to pick a word
    # Get the guess
    current_answer = input(f"Enter your {colored.fg('green')}WORDLE{colored.attr('reset')} word here: ").lower()
    while True:
        # Check if the guess is in the answer list
        if len(current_answer) != 5:
            current_answer = input("Hey, not fair. You have to enter a 5 letter word: ").lower()
        elif current_answer not in answer_list and STRICT_MODE:
            current_answer = input(f"Strict mode is on, you have to enter a valid {colored.fg('green')}WORDLE{colored.attr('reset')} word: ").lower()
        elif current_answer not in guess_list:
            current_answer = input(f"Hey, not fair. You have to at least enter a valid {colored.fg('green')}WORDLE{colored.attr('reset')} guess: ").lower()
        else:
            break

    # allow other players to make guesses
    while True:
        os.system('clear')

        ROUND_OVER = True
        for index, player in enumerate(players):
            if not player.completed and len(player.guess_list) < 6 and index != turn:
                ROUND_OVER = False
                break

        if ROUND_OVER:
            break

        pind = get_next_guess(players, turn)

        if pind == -2:
            player_to_edit = edit_prev_guesses(players, turn)
            if player_to_edit != -2:
                edit_player(players, player_to_edit)
            continue
        elif pind == -3:
            add_player(players)
            continue
        elif pind == -4:
            player_id = choose_player_to_delete(players)
            if player_id != -1:
                if player_id == turn:
                    turn = 0
                elif player_id < turn:
                    turn -= 1

            continue
        elif pind == -5:
            reorder_players(players)
            continue

        # show the last gueses the player has made
        if len(players[pind].guess_list) > 0:
            print(f"\n{colored.fg('yellow')}{players[pind].name}'s{colored.attr('reset')} last guess(es):")
            colors_list = []
            for guess in players[pind].guess_list:
                colors_list.append(gen_colors(guess, current_answer))

            i = 0
            while i < len(players[pind].guess_list):
                for index, char in enumerate(players[pind].guess_list[i]):
                    if colors_list[i][index] == 'b':
                        print(black + char + reset, end="")
                    elif colors_list[i][index] == 'y':
                        print(yellow + char + reset, end="")
                    elif colors_list[i][index] == 'g':
                        print(green + char + reset, end="")
                print()
                i += 1

        guess = input(f"Enter {colored.fg('yellow')}{players[pind].name}'s{colored.attr('reset')} guess here: ").lower()
        CANCEL_FLAG = False
        while True:
            if guess == 'cancel':
                print("Cancelling guess...")
                time.sleep(0.75)
                CANCEL_FLAG = True
                break
            elif len(guess) != 5:
                guess = input(f"{players[pind].name}'s guess must be 5 letters: ").lower()
            elif guess not in guess_list:
                guess = input(f"{players[pind].name}'s guess must be a valid {colored.fg('green')}WORDLE{colored.attr('reset')} guess: ").lower()
            else:
                break

        if CANCEL_FLAG == True:
            continue

        players[pind].guess_list.append(guess)

        # get the colors for the guess
        colors = gen_colors(guess, current_answer)

        print(f"Tell {players[pind].name} that the colors were {get_full_color_str(colors)}.")
        if players[pind].guess_list[-1] == current_answer:
            players[pind].completed = True
        input("Press ENTER to continue.")

    print(f"That concludes {players[turn].name}'s turn!")
    print(f"The word was {current_answer}.")

    # round summary
    print("\nSummary:")
    for index, player in enumerate(players):
        if index == turn:
            continue

        if not player.completed:
            print(f"{colored.fg('yellow')}{player.name}{colored.attr('reset')} did not guess the word in time:")
            player.score += 7
        else:
            print(f"{colored.fg('yellow')}{player.name}{colored.attr('reset')} guessed the word in {len(player.guess_list)} guesses.")
            player.score += len(player.guess_list)

        colors_list = []
        for guess in player.guess_list:
            colors_list.append(gen_colors(guess, current_answer))

        i = 0
        while i < len(player.guess_list):
            for index, char in enumerate(player.guess_list[i]):
                if colors_list[i][index] == 'b':
                    print(black + char + reset, end="")
                elif colors_list[i][index] == 'y':
                    print(yellow + char + reset, end="")
                elif colors_list[i][index] == 'g':
                    print(green + char + reset, end="")
            print()
            i += 1

        print()

    # show the scores
    pcopy = players.copy()
    pcopy.sort(key=lambda x: x.score, reverse=False)

    print("\nRankings:")
    suffix = ""
    for index, player in enumerate(pcopy):
        if index == 0:
            suffix = "st"
        elif index == 1:
            suffix = "nd"
        elif index == 2:
            suffix = "rd"
        else:
            suffix = "th"

        print(f"{index+1}{suffix}. {player.name} - {player.score}")

    for player in players:
        player.guess_list = []
        player.completed = False

    turn += 1
    if turn == len(players):
        turn = 0

    print()
    input("Press ENTER to play another round.")
