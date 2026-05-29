# Ping Pong (C++ / ncurses)

Классическая игра «Ping Pong» в терминале. Написана на C++17, использует библиотеку `ncurses`.

## Возможности

- Два режима: **Player vs AI** и **Player vs Player**
- Управление: `W` / `S` (игрок 1), стрелки `↑` / `↓` (игрок 2)
- Отскок мяча зависит от точки контакта с ракеткой (как в настоящем Pong)
- Счёт до 7 побед
- Пауза, рестарт, выход
- Авто-подбор размера поля под окно терминала

## Требования

- Компилятор C++17 (`g++` ≥ 7 или `clang++`)
- Библиотека `ncurses`

### Установка зависимостей

**macOS:** входит в Command Line Tools (`xcode-select --install`).

**Ubuntu / Debian:**
```bash
sudo apt update && sudo apt install -y build-essential libncurses-dev
```

**Fedora:** `sudo dnf install gcc-c++ ncurses-devel`

**Arch Linux:** `sudo pacman -S base-devel ncurses`

## Сборка и запуск

```bash
make
./pong
```

или одной командой:

```bash
make run
```

Без `make`:

```bash
g++ -std=c++17 -O2 -Wall -Wextra pong.cpp -o pong -lncurses
./pong
```

## Управление

| Клавиша      | Действие                       |
| ------------ | ------------------------------ |
| `1` / `2`    | Выбор режима в стартовом меню  |
| `W` / `S`    | Игрок 1 (левая ракетка)        |
| `↑` / `↓`    | Игрок 2 (правая ракетка)       |
| `P`          | Пауза                          |
| `R`          | Перезапуск матча               |
| `Q`          | Выход                          |

## CI

Сборка автоматически проверяется в GitHub Actions: см. `.github/workflows/cpp.yml` в корне репозитория. Workflow собирает Pong и все 7 C++ лабораторных под Ubuntu и публикует бинарники как артефакты.
