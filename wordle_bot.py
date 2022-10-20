from wordle_funcs import *
import colored as c
import math
from typing import List, Tuple

def get_entropy(words_remaining):
    return math.log2(words_remaining)

def get_prob(sel_words, total_words):
    return float(sel_words) / float(total_words)

def next_char(char : str) -> Tuple[str, bool]:
    if char == "a":
        return "b", False
    elif char == "b":
        return "c", False
    elif char == "c":
        return "a", True
    else:
        raise ValueError("next_char error, input char must be a, b, or c.")

def get_next_color(curr_color : List[str]):
    place = len(curr_color)-1
    while True:
        result = next_char(curr_color[place])
        curr_color[place] = result[0] 

        if result[1] == False:
            break

        place -= 1

        if place < 0:
            break

# COLOR CODE
# a = dark
# b = yellow
# c = green
STARTING_COLOR = ["a", "a", "a", "a", "a"]

answer_list = get_answer_list()
guess_list = get_guess_list()

print(f"Welcome to the {c.fg('yellow')}WORDLE BOT 1.0{c.attr('reset')}!")
# guess loop
while True:
    for word in guess_list:
        curr_color = STARTING_COLOR[:]
        pass
