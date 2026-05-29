// Лабораторная работа №7
// Тема: Подпрограммы. Функции.
// Задание: реализовать функцию вычисления факториала, функцию вычисления
//          степени числа и функцию числа сочетаний C(n, k) = n! / (k! * (n - k)!)
//          на её основе. Проверить на нескольких наборах входных данных.

#include <iostream>

unsigned long long factorial(int n) {
    unsigned long long result = 1ULL;
    for (int i = 2; i <= n; ++i) {
        result *= static_cast<unsigned long long>(i);
    }
    return result;
}

unsigned long long power(int base, int exp) {
    unsigned long long result = 1ULL;
    for (int i = 0; i < exp; ++i) {
        result *= static_cast<unsigned long long>(base);
    }
    return result;
}

unsigned long long combinations(int n, int k) {
    if (k < 0 || k > n) return 0ULL;
    if (k == 0 || k == n) return 1ULL;
    if (k > n - k) k = n - k;
    unsigned long long result = 1ULL;
    for (int i = 1; i <= k; ++i) {
        result = result * static_cast<unsigned long long>(n - k + i)
                 / static_cast<unsigned long long>(i);
    }
    return result;
}

int main() {
    int n = 0;
    int k = 0;
    std::cout << "Lab 7: functions. Enter n and k (0 <= k <= n <= 20): ";
    std::cin >> n >> k;
    if (n < 0 || k < 0 || k > n || n > 20) {
        std::cerr << "Invalid input." << std::endl;
        return 1;
    }

    std::cout << n << "! = " << factorial(n) << "\n"
              << k << "! = " << factorial(k) << "\n"
              << n << "^" << k << " = " << power(n, k) << "\n"
              << "C(" << n << ", " << k << ") = " << combinations(n, k) << std::endl;
    return 0;
}
