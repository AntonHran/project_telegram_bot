import csv
import datetime
import random


def form_quote(time: datetime.time) -> str:
    lst = []
    with open("quotes.csv", "r", encoding="utf-8") as file:
        reader = csv.DictReader(file, fieldnames=["quote", "author"], quoting=1)
        for row in reader:
            lst.append(row)
    res = random.choice(lst)
    return f"{res['quote']} | Author: {res['author']}. at time {time}"
