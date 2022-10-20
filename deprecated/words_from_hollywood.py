base_word = "regret"
arr = []
for letter in base_word:
    arr.append(letter)
base_word = arr
from words import get_words

five_letter_words = get_words()

best_word = ""
best_word_result = []
answers = []

for base_word in five_letter_words:
    arr = []
    for letter in base_word:
        arr.append(letter)
    base_word = arr

    for word in five_letter_words:
        clone = base_word[:]
        try:
            for letter in word:
                clone.remove(letter)
            
            answers.append(word)
        except:
            continue

    if len(answers) > len(best_word_result):
        best_word_result = answers
        best_word = base_word
    
    answers = []

print(best_word)
print(best_word_result)
