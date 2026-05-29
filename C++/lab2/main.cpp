// Лабораторная работа №2
// Тема: Программирование алгоритмов разветвлённой структуры.
// Задание: по координатам точки (x, y) определить её положение
//          относительно круга радиуса R с центром в начале координат:
//          - внутри области;
//          - вне области;
//          - на границе области.

#include <iostream>
#include <cmath>

int main() {
    double x = 0.0;
    double y = 0.0;
    double r = 0.0;

    std::cout << "Lab 2: point in circle. Enter radius R: ";
    std::cin >> r;
    std::cout << "Enter coordinates x and y: ";
    std::cin >> x >> y;

    if (r <= 0) {
        std::cerr << "Error: radius must be > 0." << std::endl;
        return 1;
    }

    const double dist = std::sqrt(x * x + y * y);
    const double epsilon = 1e-9;

    if (dist < r - epsilon) {
        std::cout << "Result: point is INSIDE the circle." << std::endl;
    } else if (dist > r + epsilon) {
        std::cout << "Result: point is OUTSIDE the circle." << std::endl;
    } else {
        std::cout << "Result: point is ON the circle border." << std::endl;
    }

    return 0;
}
