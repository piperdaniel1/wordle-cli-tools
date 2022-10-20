import sys

args = sys.argv

if len(args) != 2 and len(args) != 3:
    print("Usage: python3 list_analyzer.py <list_file> [<master_list_file>]")
    sys.exit(1)

list_file = args[1]
master_list_file = args[2] if len(args) == 3 else 'words.txt'

try:
    with open(list_file, "r") as f:
        list_file = f.readlines()

    with open(master_list_file, "r") as f:
        master_list = f.readlines()
except FileNotFoundError:
    print("Error: Passed file not found")
    sys.exit(1)

list_file = [x.strip() for x in list_file]
master_list = [x.strip() for x in master_list]

missing_words = []
for word in list_file:
    if word not in master_list:
        missing_words.append(word)

if len(missing_words) > 0:
    print("The following words are missing from the master list:")
    for index, word in enumerate(missing_words):
        print(f"{index} - {word}")
else:
    print("All words are present in the master list, exiting...")
    sys.exit(0)

while True:
    choice = input("\nEnter an index to remove from the list or 'q' to quit, or 'a' to add the words to the master list: ")

    try:
        choice = int(choice)

        if choice < 0 or choice >= len(missing_words):
            print("Error: Index out of range")
            continue
        
        print(f"Removing {missing_words[choice]} from the list")
        list_file.remove(missing_words[choice])
    except ValueError:
        if choice == 'q':
            sys.exit(0)
        elif choice == 'a':
            with open(master_list_file, "a") as f:
                for word in missing_words:
                    f.write(f"{word}\n")
            print("Words added to master list, exiting...")
            sys.exit(0)
