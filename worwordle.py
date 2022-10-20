from wordle_funcs import *
wordle_words = get_answer_list()
letters = ["a", "t", "o", "n", "e"]

for word in wordle_words:
    overlaps = 0
    for letter in letters:
        if letter in word:
            overlaps += 1

    if "i" in word and "u" in word:
        print(word)
