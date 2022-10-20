import colored

def is_syntactically_correct(input_string: str):
    for i in range(len(input_string)-1):
        if (input_string[i] == '+' or input_string[i] == '-') and (input_string[i+1] == '+' or input_string[i+1] == '-'):
            return False

        if (input_string[i] == '*' or input_string[i] == '/') and (input_string[i+1] == '*' or input_string[i+1] == '/'):
            return False
    
    return True


green = colored.bg('green')
yellow = colored.bg('yellow')
black = colored.bg('black')
reset = colored.attr('reset')

test_guesses = ["43+12=55", "7*8+4=60"]
test_colors =  ["ybybbgbb", "byyyygyb"]

print("Welcome to the Nerdle Solve 2.0!")
print("Nerdle Solve 2.0 is like World Solve 2.0 but for Nerdle.")

print("\nWe'll start by having you write the guesses that you save done so far.")

guesses = []
colors_list = []
check = ""

while True:
    print("\nEnter your next guess if you would like...")
    while True:
        word = input(f"Guess #{len(guesses)+1}: ")
        if word == "t":
            word = test_guesses.pop(0)

        if word == "":
            break

        if len(word) != 8:
            print("Each guess must be eight letters. Input not counted.")
            continue

        guesses.append(word)

    print("\nNice! Now we'll record the colors that resulted from those guesses.")

    colors = ""
    while len(colors_list) != len(guesses):
        colors = input(f"Colors from guess #{len(colors_list)+1}: ")
        colors = colors.lower()
        if colors == "t":
            colors = test_colors.pop(0)

        if len(colors) != 8:
            print("Sorry, all inputs must be eight letters. Input not counted.")
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

    #
    # Solver part of code
    #
    base_chars = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+', '-', '*', '/', '=']
    digit_chars = [base_chars[:] for i in range(8)]

    must_have_chars = set()

    # Naive way to get rid of as many possiblities as you can
    # if you only consider each digit seperately
    for i in range(8):
        for j in range(len(guesses)):
            if colors_list[j][i] == 'b':
                for digit in digit_chars:
                    try:
                        if guesses[j][i] not in must_have_chars:
                            digit.remove(guesses[j][i])
                    except ValueError:
                        pass

            elif colors_list[j][i] == 'y':
                try:
                    digit_chars[i].remove(guesses[j][i])
                    must_have_chars.add(guesses[j][i])
                except ValueError:
                    pass

            elif colors_list[j][i] == 'g':
                try:
                    digit_chars[i] = [guesses[j][i]]
                    must_have_chars.add(guesses[j][i])

                    '''for index, digit in enumerate(digit_chars):
                        try:
                            if index != i:
                                digit.remove(guesses[j][i])
                        except ValueError:
                            pass'''
                except ValueError:
                    pass
    
    # Print out possible digits
    print("Narrowed down digits:")
    max = 0
    for digit in digit_chars:
        if len(digit) > max:
            max = len(digit)

    print("x " * 8)
    for i in range(max):
        for digit in digit_chars:
            if len(digit) > i:
                print(digit[i], end=" ")
            else:
                print("  ", end="")
        print()
    
    total = len(digit_chars[0]) * len(digit_chars[1]) * len(digit_chars[2]) * len(digit_chars[3]) * len(digit_chars[4]) * len(digit_chars[5]) * len(digit_chars[6]) * len(digit_chars[7])
    print("With brute force, there are " + str(total) + " possible solutions.")
    input("Press enter to print all possibilities...")
    count = 0
    possible_answers = []
    for i1, d1 in enumerate(digit_chars[0]):
        for i2, d2 in enumerate(digit_chars[1]):
            for i3, d3 in enumerate(digit_chars[2]):
                for i4, d4 in enumerate(digit_chars[3]):
                    for i5, d5 in enumerate(digit_chars[4]):
                        for i6, d6 in enumerate(digit_chars[5]):
                            for i7, d7 in enumerate(digit_chars[6]):
                                for i8, d8 in enumerate(digit_chars[7]):
                                    count += 1
                                    if count % 10000 == 0:
                                        print(f"Analyzing solutions, {round(count/total*100)}% complete...         ", end="\r")
                                    try:
                                        possible_str = str(d1) + str(d2) + str(d3) + str(d4) + str(d5) + str(d6) + str(d7) + str(d8)
                                        split_str = possible_str.split("=")
                                        if len(split_str) == 2:
                                            left_side = eval(split_str[0])
                                            right_side = eval(split_str[1])

                                            if left_side == right_side and right_side > 0:
                                                if len(str(right_side)) == len(split_str[1]):
                                                    missing_yellow = False
                                                    for yellow_char in must_have_chars:
                                                        if yellow_char not in possible_str:
                                                            missing_yellow = True
                                                            break
                                                    
                                                    if not missing_yellow:
                                                        if is_syntactically_correct(possible_str):
                                                            possible_answers.append(possible_str)
                                    except:
                                        pass

    print("Complete. Possible answers:                  ")
    print(possible_answers)
    print(f"There are {len(possible_answers)} possible answers.")