"""Лабораторная работа №1 (Python).

Тема: Управляющие символы ANSI и вывод в консоль.
Вариант: 1 (Франция, узор «a», функция y = x^2, условие — количество
чисел из sequence.txt, меньших и больших нуля).

Программа последовательно:
1) рисует флаг Франции ANSI-цветами;
2) выводит повторяющийся узор;
3) строит график y = x^2 в первом квадранте (>= 9 строк);
4) загружает (или генерирует синтетический) sequence.txt и выводит
   диаграмму процентного соотношения чисел < 0 и > 0.
"""

from __future__ import annotations

import os
import random
import sys

RESET = "\033[0m"


def color_block(rgb_bg: str, width: int = 8) -> str:
    return f"\033[48;2;{rgb_bg}m{' ' * width}{RESET}"


def draw_france_flag() -> None:
    print("== Flag of France ==")
    blue = "0;85;164"
    white = "255;255;255"
    red = "239;65;53"
    height = 6
    block_w = 10
    for _ in range(height):
        line = (
            color_block(blue, block_w)
            + color_block(white, block_w)
            + color_block(red, block_w)
        )
        print(line)
    print()


def draw_pattern(rows: int = 6, cols: int = 30) -> None:
    """Узор «a»: чередование цветов клетками 2x2."""
    print("== Pattern A ==")
    palette = ["\033[41m  ", "\033[44m  ", "\033[42m  ", "\033[43m  "]
    for r in range(rows):
        line = "".join(palette[(r + c) % len(palette)] for c in range(cols))
        print(line + RESET)
    print()


def draw_function_plot(width: int = 11, height: int = 11) -> None:
    """График y = x^2 в первом квадранте, минимум 9 строк."""
    print("== Plot: y = x^2 ==")
    grid = [[" " for _ in range(width)] for _ in range(height)]
    max_y = (width - 1) ** 2
    for x in range(width):
        y = x * x
        row = height - 1 - int(round((y / max_y) * (height - 1)))
        if 0 <= row < height:
            grid[row][x] = "*"
    for row in grid:
        print("|" + "".join(row))
    print("+" + "-" * width)
    print()


def load_sequence(path: str = "sequence.txt") -> list[float]:
    if not os.path.exists(path):
        random.seed(42)
        with open(path, "w", encoding="utf-8") as fh:
            for _ in range(250):
                fh.write(f"{random.uniform(-10, 10):.3f}\n")
    with open(path, "r", encoding="utf-8") as fh:
        return [float(line.strip()) for line in fh if line.strip()]


def draw_percentage_diagram(seq: list[float]) -> None:
    print("== Distribution of numbers in sequence.txt ==")
    total = len(seq)
    if total == 0:
        print("(empty sequence)")
        return
    less = sum(1 for x in seq if x < 0)
    greater = sum(1 for x in seq if x > 0)
    zero = total - less - greater

    bar_width = 40

    def bar(label: str, count: int) -> str:
        pct = count / total * 100
        filled = int(round(pct / 100 * bar_width))
        return f"{label:>10}: [{'#' * filled}{'.' * (bar_width - filled)}] {pct:5.1f}% ({count})"

    print(bar("< 0", less))
    print(bar("> 0", greater))
    print(bar("== 0", zero))
    print()


def main() -> int:
    draw_france_flag()
    draw_pattern()
    draw_function_plot()
    seq = load_sequence(os.path.join(os.path.dirname(__file__) or ".", "sequence.txt"))
    draw_percentage_diagram(seq)
    return 0


if __name__ == "__main__":
    sys.exit(main())
