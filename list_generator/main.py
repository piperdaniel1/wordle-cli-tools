from datetime import date, timedelta as td
import requests

def main():
    BASE_URL = "https://www.nytimes.com/svc/wordle/v2/"
    curr_day = date.today() + td(1)
    date_str = curr_day.strftime("%Y-%m-%d") + ".json"

    # Get the data
    url = BASE_URL + date_str
    print(url)
    r = requests.get(url)

    print(r)

    # Parse the data
    data = r.json()
    print(data)

if __name__ == '__main__':
    main()
