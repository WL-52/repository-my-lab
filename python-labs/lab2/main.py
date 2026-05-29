"""Лабораторная работа №2 (Python).

Тема: Работа с табличными форматами (CSV и XML).
Вариант: 1.

CSV: фильтрация книг до 150 рублей, поиск по автору, генерация
библиографических ссылок 20 произвольных книг в bibliography.txt.
XML: парсинг файла валют и формирование словаря {Name -> Value}.

Если books.csv / currency.xml отсутствуют рядом со скриптом — программа
создаёт небольшие синтетические файлы для демонстрации.
"""

from __future__ import annotations

import csv
import os
import random
import xml.dom.minidom as minidom
from pathlib import Path


HERE = Path(__file__).resolve().parent
BOOKS_CSV = HERE / "books.csv"
CURRENCY_XML = HERE / "currency.xml"
BIBLIO_TXT = HERE / "bibliography.txt"


def ensure_books_csv() -> None:
    if BOOKS_CSV.exists():
        return
    sample = [
        ["author", "title", "year", "price"],
        ["Pushkin A.S.", "Eugene Onegin", "2014", "120"],
        ["Tolstoy L.N.", "War and Peace", "2018", "650"],
        ["Dostoevsky F.M.", "Crime and Punishment", "2017", "400"],
        ["Pushkin A.S.", "The Captain's Daughter", "2015", "140"],
        ["Bulgakov M.A.", "The Master and Margarita", "2019", "550"],
        ["Chekhov A.P.", "Short Stories", "2013", "95"],
        ["Gogol N.V.", "Dead Souls", "2016", "320"],
        ["Lermontov M.Y.", "A Hero of Our Time", "2015", "130"],
        ["Turgenev I.S.", "Fathers and Sons", "2018", "280"],
        ["Pasternak B.L.", "Doctor Zhivago", "2020", "720"],
    ]
    with BOOKS_CSV.open("w", newline="", encoding="utf-8") as fh:
        csv.writer(fh, delimiter=";").writerows(sample)


def ensure_currency_xml() -> None:
    if CURRENCY_XML.exists():
        return
    xml = """<?xml version='1.0' encoding='utf-8'?>
<ValCurs>
  <Valute><NumCode>840</NumCode><CharCode>USD</CharCode><Nominal>1</Nominal><Name>US Dollar</Name><Value>91,5</Value></Valute>
  <Valute><NumCode>978</NumCode><CharCode>EUR</CharCode><Nominal>1</Nominal><Name>Euro</Name><Value>99,2</Value></Valute>
  <Valute><NumCode>826</NumCode><CharCode>GBP</CharCode><Nominal>1</Nominal><Name>Pound Sterling</Name><Value>116,8</Value></Valute>
  <Valute><NumCode>392</NumCode><CharCode>JPY</CharCode><Nominal>100</Nominal><Name>Japanese Yen</Name><Value>59,3</Value></Valute>
  <Valute><NumCode>156</NumCode><CharCode>CNY</CharCode><Nominal>1</Nominal><Name>Yuan Renminbi</Name><Value>12,6</Value></Valute>
</ValCurs>
"""
    CURRENCY_XML.write_text(xml, encoding="utf-8")


def read_books() -> list[dict[str, str]]:
    with BOOKS_CSV.open(encoding="utf-8") as fh:
        return list(csv.DictReader(fh, delimiter=";"))


def filter_cheap(books: list[dict[str, str]], limit: int = 150) -> list[dict[str, str]]:
    return [b for b in books if int(b["price"]) <= limit]


def find_by_author(books: list[dict[str, str]], author: str, limit: int = 5) -> list[dict[str, str]]:
    needle = author.lower()
    found = [b for b in books if needle in b["author"].lower()]
    return found[:limit]


def generate_bibliography(books: list[dict[str, str]], count: int = 20) -> None:
    sample = random.sample(books, k=min(count, len(books)))
    with BIBLIO_TXT.open("w", encoding="utf-8") as fh:
        for i, b in enumerate(sample, start=1):
            fh.write(f"{i}. {b['author']}. {b['title']} - {b['year']}\n")
    print(f"Bibliography saved to {BIBLIO_TXT.name} ({len(sample)} entries)")


def parse_currency() -> dict[str, float]:
    dom = minidom.parse(str(CURRENCY_XML))
    result: dict[str, float] = {}
    for v in dom.getElementsByTagName("Valute"):
        name_node = v.getElementsByTagName("Name")[0].firstChild
        value_node = v.getElementsByTagName("Value")[0].firstChild
        if name_node and value_node:
            value = float(value_node.data.replace(",", "."))
            result[name_node.data] = value
    return result


def main() -> int:
    ensure_books_csv()
    ensure_currency_xml()
    books = read_books()

    print(f"Total books: {len(books)}")
    cheap = filter_cheap(books, 150)
    print(f"Books up to 150 rub: {len(cheap)}")
    for b in cheap:
        print(f"  {b['author']} - {b['title']} ({b['year']}, {b['price']} rub)")

    print()
    print("Search by author 'Pushkin':")
    for b in find_by_author(books, "Pushkin"):
        print(f"  {b['author']} - {b['title']}")

    print()
    generate_bibliography(books, 20)

    print()
    print("Currency dictionary (Name -> Value):")
    for name, value in parse_currency().items():
        print(f"  {name:>20} : {value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
