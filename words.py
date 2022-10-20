def get_words():
    with open('words.txt', 'r') as f:
        words = f.readlines()

    return [word.replace("\n", "") for word in words]

def get_guess_list():
    with open('all_guesses.txt', 'r') as f:
        guesses = f.readlines()

    return [guess.replace("\n", "") for guess in guesses]

def get_answer_list():
    with open('answer_list.txt', 'r') as f:
        answers = f.readlines()

    return [answer.replace("\n", "") for answer in answers]
