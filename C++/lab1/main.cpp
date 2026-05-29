// Лабораторная работа №1
// Тема: Программирование алгоритмов линейной структуры.
// Задание: вычислить значение выражения Y = (a + b) / (a * b) + pow(a, 2)
//          Использовать два варианта ввода-вывода: библиотека функций C
//          (scanf/printf) и библиотека классов C++ (cin/cout).

#include <cstdio>
#include <cmath>
#include <iostream>
#include <iomanip>

int main() {
    double a = 0.0;
    double b = 0.0;

    std::printf("Lab 1: linear program. Enter a and b (e.g. 1.5 2.3): ");
    if (std::scanf("%lf %lf", &a, &b) != 2) {
        std::fprintf(stderr, "Invalid input.\n");
        return 1;
    }

    const double y = (a + b) / (a * b) + std::pow(a, 2);

    std::printf("[C-style ] a = %.4f, b = %.4f, Y = %.6f\n", a, b, y);

    std::cout << std::fixed << std::setprecision(6)
              << "[C++-style] a = " << a
              << ", b = " << b
              << ", Y = " << y << std::endl;

    return 0;
}
