import csv

from bs4 import BeautifulSoup
import requests


def scrap_quotes():
    page = "https://www.oberlo.com/blog/motivational-quotes"
    res = requests.get(page)
    soup = BeautifulSoup(res.text, "lxml")
    quotes = soup.select("li")
    q = [
        quote.text.replace("“", "")
        .replace("”", "")
        .replace("―", "-")
        .replace("—", "-")
        .replace("–", "-")
        for quote in quotes
        if quote.text.startswith("“")
    ]
    # [print(el) for el in q]
    with open("quotes.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["quote", "author"], quoting=1)
        writer.writeheader()
        for quote in q:
            try:
                qu, author = quote.rsplit("-", 1)
            except ValueError:
                pass
            writer.writerow({"quote": qu.strip(), "author": author.strip()})
