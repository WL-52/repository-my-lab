# Материалы к диффзачету — Ожигов Сергей

Здесь собраны все работы для допуска к диффзачету по дисциплине "Основы алгоритмизации и программированию".

Сайт с портфолио и резюме: https://WL-52.github.io/repository-my-lab/

## Что здесь лежит

- Web-Site/ - HTML-сайт с резюме на русском и английском
- ping-pong-cpp/ - игра Ping Pong на C++ (в терминале)
- C++/ - 7 лабораторных работ по C++
- python-labs/ - 6 лабораторных работ по Python
- telegram-bot/ - бот для сдачи домашки преподу
- HTML/ - 17 заданий по HTML

## Проекты

### Ping Pong (C++)

Аркадная игра в терминале. Есть режим игрок против игрока и игрок против компьютера.
Собирается командой make.

    cd ping-pong-cpp
    make
    ./pong

Подробнее: ping-pong-cpp/README.md

### Telegram-бот "Сдача ДЗ"

Бот для колледжа. Студент пишет /submit, выбирает предмет, пишет комментарий,
прикрепляет файл и отправляет. Бот пересылает все преподавателю.

Запуск:

    cd telegram-bot
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt

Нужно создать файл .env и вписать туда BOT_TOKEN (получить у @BotFather)
и TEACHER_CHAT_ID (узнать через @userinfobot).

    cp .env.example .env

Потом:

    export BOT_TOKEN="..."
    export TEACHER_CHAT_ID="..."
    python3 bot.py

Команды: /start, /submit, /list, /help, /cancel

Подробнее: telegram-bot/README.md

## Лабораторные работы по C++

1. Линейные алгоритмы (ввод-вывод C-style и C++-style) - C++/lab1/main.cpp
2. Ветвление (точка относительно круга) - C++/lab2/main.cpp
3. Циклы while / do-while (сумма ряда) - C++/lab3/main.cpp
4. Цикл for + одномерный массив - C++/lab4/main.cpp
5. Двумерный массив + указатели - C++/lab5/main.cpp
6. Строки - C++/lab6/main.cpp
7. Функции (факториал + сочетания) - C++/lab7/main.cpp

Собрать все:

    cd C++
    make

Запустить:

    ./lab1/lab
    ./lab2/lab
    ...

## Лабораторные работы по Python

1. ANSI и вывод в консоль - python-labs/lab1/main.py
2. CSV и XML - python-labs/lab2/main.py
3. Tkinter (генератор ключей) - python-labs/lab3/main.py
4. Задача о рюкзаке (жадный + динамическое программирование) - python-labs/lab4/main.py
5. Регулярные выражения - python-labs/lab5/main.py
6. ООП (Person -> Student/Teacher, класс Group) - python-labs/lab6/main.py

Запуск:

    python3 python-labs/lab1/main.py
    python3 python-labs/lab2/main.py
    ...

## Задания по HTML

17 практических работ. Открыть оглавление: HTML/index.html

## GitHub Actions

В папке .github/workflows лежат 3 workflow:
- pages.yml - публикует сайт на GitHub Pages
- cpp.yml - собирает Pong и лабы на Linux
- python.yml - проверяет Python-лабы и бота

После первого пуша в main нужно включить Pages:
Settings -> Pages -> Source = GitHub Actions

## Резюме

На сайте: Web-Site/resume.html (RU + EN)
PDF в корне репозитория:
- Resume Udin.docx.pdf (английский)
- Резюме Юдин.docx (1).pdf (русский)

## Источники заданий

- Литвинская О.С. и др. "Основы программирования на языке C++". Методичка к лабораторным. Пенза, 2017. (файл metodichpipo (1).pdf)
- Лабораторный практикум 1-6 по Python (файл .docx)
- Практические работы по HTML (файл html_tasks.pdf)

## Как запушить на GitHub

    cd "Ozhigov-Sergey"
    git init
    git add .
    git commit -m "Initial commit"
    git branch -M main
    git remote add origin https://github.com/WL-52/repository-my-lab.git
    git push -u origin main

Потом зайти в Settings -> Pages и выбрать GitHub Actions.
