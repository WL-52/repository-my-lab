// Лабораторная работа №5
// Тема: Обработка двумерных массивов. Указатели.
// Задание (вариант 1): вычислить сумму отрицательных элементов каждого
//          столбца матрицы A(m x n). Доступ к элементам реализован через
//          указатели для демонстрации связи массивов и указателей.

#include <iostream>
#include <vector>

int main() {
    int m = 0;
    int n = 0;
    std::cout << "Lab 5: enter matrix dimensions m and n (rows and columns): ";
    std::cin >> m >> n;
    if (m <= 0 || n <= 0) {
        std::cerr << "Dimensions must be positive." << std::endl;
        return 1;
    }

    std::vector<int> a(static_cast<size_t>(m) * n);
    int* const data = a.data();

    std::cout << "Enter " << m * n << " matrix elements row by row:" << std::endl;
    for (int i = 0; i < m * n; ++i) {
        if (!(std::cin >> data[i])) {
            std::cerr << "Invalid input." << std::endl;
            return 1;
        }
    }

    std::cout << "Sum of negative elements per column:" << std::endl;
    for (int col = 0; col < n; ++col) {
        long long sum = 0;
        for (int row = 0; row < m; ++row) {
            const int* p = data + row * n + col;
            if (*p < 0) sum += *p;
        }
        std::cout << "  column " << col << ": " << sum << "\n";
    }

    return 0;
}
