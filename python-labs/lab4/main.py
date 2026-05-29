"""Лабораторная работа №4 (Python).

Тема: Задача о рюкзаке.

Реализованы два варианта решения задачи о рюкзаке (knapsack):
1) Жадный алгоритм по убыванию плотности value/weight (быстрое
   приближённое решение, приведено для сравнения).
2) Точное решение методом динамического программирования (0/1 knapsack)
   с восстановлением списка выбранных предметов.

Программа выводит сравнение результатов обоих методов на наборе тестовых
данных и позволяет передать собственный набор через консоль.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class Item:
    name: str
    weight: int
    value: int


def greedy_knapsack(items: Iterable[Item], capacity: int) -> tuple[int, list[Item]]:
    chosen: list[Item] = []
    total_value = 0
    remaining = capacity
    sorted_items = sorted(items, key=lambda it: it.value / it.weight, reverse=True)
    for it in sorted_items:
        if it.weight <= remaining:
            chosen.append(it)
            remaining -= it.weight
            total_value += it.value
    return total_value, chosen


def dp_knapsack(items: list[Item], capacity: int) -> tuple[int, list[Item]]:
    n = len(items)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        w_i = items[i - 1].weight
        v_i = items[i - 1].value
        for w in range(capacity + 1):
            dp[i][w] = dp[i - 1][w]
            if w_i <= w:
                cand = dp[i - 1][w - w_i] + v_i
                if cand > dp[i][w]:
                    dp[i][w] = cand

    chosen: list[Item] = []
    w = capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            chosen.append(items[i - 1])
            w -= items[i - 1].weight
    chosen.reverse()
    return dp[n][capacity], chosen


def print_solution(label: str, total: int, chosen: list[Item], capacity: int) -> None:
    used_weight = sum(it.weight for it in chosen)
    print(f"{label}: total value = {total}, used weight = {used_weight}/{capacity}")
    for it in chosen:
        print(f"  - {it.name:<12} w={it.weight:<3} v={it.value}")
    print()


def main() -> int:
    items = [
        Item("laptop",     3, 2000),
        Item("camera",     1,  500),
        Item("book",       2,  300),
        Item("food-pack",  4,  600),
        Item("tent",       6,  800),
        Item("flashlight", 1,  150),
        Item("water",      3,  450),
        Item("first-aid",  2,  700),
    ]
    capacity = 10

    print(f"Knapsack capacity = {capacity}")
    print(f"Items count       = {len(items)}\n")

    g_total, g_chosen = greedy_knapsack(items, capacity)
    print_solution("Greedy (approx.)", g_total, g_chosen, capacity)

    dp_total, dp_chosen = dp_knapsack(items, capacity)
    print_solution("Dynamic programming (exact)", dp_total, dp_chosen, capacity)

    if dp_total >= g_total:
        print(f"DP is at least as good as greedy: gap = {dp_total - g_total}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
