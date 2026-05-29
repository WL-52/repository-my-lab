// Лабораторная работа №6
// Тема: Строки.
// Задание: дана последовательность символов S; группы символов, разделённые
//          одним или несколькими пробелами и не содержащие пробелов внутри
//          себя, считаются словами. Найти количество слов и самое длинное
//          слово в строке.

#include <iostream>
#include <string>
#include <sstream>

int main() {
    std::cout << "Lab 6: strings. Enter a line of text:" << std::endl;
    std::string line;
    std::getline(std::cin, line);

    std::istringstream iss(line);
    std::string word;
    std::string longest;
    int wordCount = 0;
    while (iss >> word) {
        ++wordCount;
        if (word.size() > longest.size()) longest = word;
    }

    std::cout << "Total words  : " << wordCount << "\n";
    std::cout << "String length: " << line.size() << " chars\n";
    if (wordCount == 0) {
        std::cout << "(no words found)" << std::endl;
    } else {
        std::cout << "Longest word : \"" << longest << "\" ("
                  << longest.size() << " chars)" << std::endl;
    }
    return 0;
}
