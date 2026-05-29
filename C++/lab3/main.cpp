// Лабораторная работа №3
// Тема: Программирование циклов с неизвестным заранее числом повторений.
// Задание: вычислить сумму ряда S = sum(1 / n^3), n = 1..N с заданной
//          точностью eps (суммирование прекращается, когда очередное
//          слагаемое становится меньше eps). Реализовать двумя способами:
//          через while и через do-while.

#include <iostream>
#include <iomanip>

int main() {
    double eps = 0.0;
    std::cout << "Lab 3: iterative loops. Enter precision eps (e.g. 1e-6): ";
    std::cin >> eps;
    if (eps <= 0) {
        std::cerr << "Precision must be positive." << std::endl;
        return 1;
    }

    double sumWhile = 0.0;
    long long n = 1;
    double term = 1.0;
    while (term >= eps) {
        sumWhile += term;
        ++n;
        term = 1.0 / (static_cast<double>(n) * n * n);
    }
    const long long iterWhile = n - 1;

    double sumDo = 0.0;
    long long m = 0;
    double t = 0.0;
    do {
        ++m;
        t = 1.0 / (static_cast<double>(m) * m * m);
        if (t < eps) break;
        sumDo += t;
    } while (true);
    const long long iterDo = m - 1;

    std::cout << std::fixed << std::setprecision(8)
              << "[ while  ] S = " << sumWhile << ", iterations = " << iterWhile << "\n"
              << "[do-while] S = " << sumDo    << ", iterations = " << iterDo    << "\n"
              << "Reference (pi^2 / 6) = " << (3.14159265358979323846 * 3.14159265358979323846 / 6.0)
              << std::endl;
    return 0;
}
