from words import get_words
import time

words = get_words()

print("Format:")
print("First five characters are lowercase and reserved for letters in correct places. Put _ if you do not know what character is in that place.")
print("After these characters put uppercase letters for characters that are in the word but you do not know where they are.")
print("After these characters put lowercase letters for characters that may be in the word but also may not be.")
print("Do not include letters that cannot be in the word.")
print("Example:")
print("f_u__RItgsha")
print("Meaning words starts with F, has a U in the middle and includes an R and I. May include t, g, s, h, a. May not incude anything else.\n")
search_term = input("Enter search string: ")

certain_chars = []
for i in range(5):
    certain_chars.append(search_term[i].lower())

contained_chars = [] # in word but we do not know where
uncertain_chars = [] # possibly in word

for i in range(5, len(search_term)):
    if search_term[i].islower():
        contained_chars.append(search_term[i].lower())
    else:
        uncertain_chars.append(search_term[i].lower())

print(f"\nAlright, searching {len(words)} words for '{search_term}'")
EXPECTED_TIME = 2.25
SLEEP_AMOUNT = EXPECTED_TIME / len(words)
print("Preparing word buffer for stage 1...")
time.sleep(0.75)
w = len(words)-1
while w >= 0:
    for i, e in enumerate(certain_chars):
        if e != words[w][i] and e != "_":
            words.pop(w)
            break

    w -= 1

    print(f"Running stage 1, {len(words)} possible words in shortlist...       ", end="\r")
    time.sleep(SLEEP_AMOUNT)

print("")
print("Preparing word buffer for stage 2...                                       ")
time.sleep(0.75)
EXPECTED_TIME = 1.5
SLEEP_AMOUNT = EXPECTED_TIME / len(words)

w = len(words)-1
while w >= 0:
    for e in contained_chars:
        if words[w].find(e) == -1:
            words.pop(w)
            break

    w -= 1
    print(f"Running stage 2, {len(words)} possible words in shortlist...        ", end="\r")
    time.sleep(SLEEP_AMOUNT)

print("")
master_arr = []
master_arr.extend(certain_chars)
master_arr.extend(contained_chars)
master_arr.extend(uncertain_chars)

EXPECTED_TIME = 2.25
SLEEP_AMOUNT = EXPECTED_TIME / len(words)

print("Preparing dense word buffer for stage 3...                                       ")
time.sleep(1.8)

w = len(words)-1
while w >= 0:
    for e in words[w]:
        try:
            master_arr.index(e)
        except ValueError:
            words.pop(w)
            break

    w -= 1
    print(f"Running stage 3, {len(words)} possible words in shortlist...        ", end="\r")
    time.sleep(SLEEP_AMOUNT)

print("\n")
if len(words) == 1:
    print(f"Awesome, only the word '{words[0]}' matches your search criteria!")
else:
    print(f"Uh oh, {len(words)} words are left after narrowing down to your search criteria.")
    for word in words:
        print(word) 
