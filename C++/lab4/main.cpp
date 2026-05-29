// Лабораторная работа №4
// Тема: Программирование циклов с параметром. Одномерные массивы.
// Задание (вариант 1): произвести следующую обработку 20 целых чисел:
//   - найти количество отрицательных чисел;
//   - найти количество нулевых элементов;
//   - подсчитать сумму положительных чисел.

#include <iostream>

int main() {
    constexpr int N = 20;
    int a[N] = {0};

    std::cout << "Lab 4: array processing. Enter " << N << " integers:" << std::endl;
    for (int i = 0; i < N; ++i) {
        if (!(std::cin >> a[i])) {
            std::cerr << "Error: invalid input at position " << i << "." << std::endl;
            return 1;
        }
    }

    int negCount = 0;
    int zeroCount = 0;
    long long posSum = 0;

    for (int i = 0; i < N; ++i) {
        if (a[i] < 0) {
            ++negCount;
        } else if (a[i] == 0) {
            ++zeroCount;
        } else {
            posSum += a[i];
        }
    }

    std::cout << "Results:\n"
              << "  Negative numbers: " << negCount << "\n"
              << "  Zeros           : " << zeroCount << "\n"
              << "  Sum of positives: " << posSum << std::endl;
    return 0;
}
