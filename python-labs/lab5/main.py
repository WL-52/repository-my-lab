"""Лабораторная работа №5 (Python).

Тема: Работа с регулярными выражениями.

Демонстрационная задача: дан текстовый отчёт о посещаемости и контактах
студентов колледжа. С помощью регулярных выражений извлекаются:

1) email-адреса;
2) телефонные номера в форматах +7 (XXX) XXX-XX-XX и 8XXXXXXXXXX;
3) даты в формате DD.MM.YYYY;
4) идентификаторы групп (например, ИС-23-1);
5) почтовые индексы (6 цифр).

При отсутствии файла report.txt рядом со скриптом он будет создан с
демонстрационным содержимым.
"""

from __future__ import annotations

import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPORT = HERE / "report.txt"

SAMPLE = """\
Отчёт о посещаемости группы ИС-23-1 за период с 01.09.2024 по 30.09.2024.

Студенты:
- Юдин Владислав, email: udinvlad44@gmail.com, тел. +7 (915) 144-02-73, индекс 109377.
- Иванов Иван, ivanov.i@mail.ru, +7 (495) 123-45-67, ДР 11.01.2008, индекс 101000.
- Петров Пётр (группа ПР-22-2), petrov_2005@yandex.ru, 89261112233, индекс 119049.

Контакты деканата: dekanat@mkdk.ru, +7 (495) 777-88-99, приём 02.10.2025 с 09:00.
"""


def ensure_report() -> None:
    if not REPORT.exists():
        REPORT.write_text(SAMPLE, encoding="utf-8")


def extract(pattern: str, text: str) -> list[str]:
    return re.findall(pattern, text)


def main() -> int:
    ensure_report()
    text = REPORT.read_text(encoding="utf-8")

    emails = extract(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
    phones_intl = extract(r"\+7\s*\(\d{3}\)\s*\d{3}-\d{2}-\d{2}", text)
    phones_8 = extract(r"\b8\d{10}\b", text)
    dates = extract(r"\b\d{2}\.\d{2}\.\d{4}\b", text)
    groups = extract(r"\b[А-Я]{2,3}-\d{2}-\d{1,2}\b", text)
    zips_ = extract(r"\b\d{6}\b", text)

    print("Emails  :", emails)
    print("Phones+7:", phones_intl)
    print("Phones 8:", phones_8)
    print("Dates   :", dates)
    print("Groups  :", groups)
    print("ZIPs    :", zips_)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
