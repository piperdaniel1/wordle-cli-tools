from datetime import datetime, timedelta
import time

with open('full_inorder_answers.txt') as f:
    lines = f.readlines()

dict_list = []

for line in lines:
    split_line = line.split(" ")
    date_str = split_line[0] + ' ' + split_line[1] + ' ' + split_line[2]
    date_dt = datetime.strptime(date_str, '%b %d %Y')
    date_dt -= timedelta(16)

    dict_list.append({
        "date": date_dt,
        "number": str(int(split_line[4])-16),
        "word": split_line[5].strip('\n'),
    })

# index 436 is number 420 (HUNKY)

with open('fixed_inorder_answers.txt', 'w') as f:
    for day in dict_list:
        f.write(f"{time.mktime(day['date'].timetuple())} {day['number']} {day['word']}\n")