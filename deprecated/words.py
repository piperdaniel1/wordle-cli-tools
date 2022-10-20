def get_words():
    with open('words.txt', 'r') as f:
        words = f.readlines()

    return [word.replace("\n", "") for word in words]

