from wordle_funcs import *
import numpy

answer_list = get_answer_list()

letters = {}
for answer in answer_list:
    for letter in answer:
        if letter in letters:
            letters[letter] += 1/len(answer_list)
        else:
            letters[letter] = 1/len(answer_list)

letters_sorted = sorted(letters.items(), key=lambda x: x[1], reverse=True)

print(letters_sorted)
for elem in letters_sorted:
    print(elem)
# for i in range(26):
#     print(chr(97 + i), letters[chr(97 + i)])

