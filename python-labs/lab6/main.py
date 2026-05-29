"""Лабораторная работа №6 (Python).

Тема: Объектно-ориентированное программирование.

Демонстрация ключевых концепций ООП:
- инкапсуляция (приватные атрибуты, свойства);
- наследование (Person -> Student / Teacher);
- полиморфизм (метод describe в подклассах);
- агрегация (Group хранит список Student'ов).

Сценарий: моделирование учебной группы колледжа. Программа создаёт
группу студентов, добавляет преподавателя, ставит оценки и выводит
статистику по группе.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from statistics import mean


class Person:
    def __init__(self, full_name: str, age: int) -> None:
        self._full_name = full_name
        self._age = age

    @property
    def full_name(self) -> str:
        return self._full_name

    @property
    def age(self) -> int:
        return self._age

    def describe(self) -> str:
        return f"Person {self._full_name}, {self._age} y.o."


class Student(Person):
    def __init__(self, full_name: str, age: int, group: str) -> None:
        super().__init__(full_name, age)
        self.group = group
        self._grades: list[int] = []

    def add_grade(self, grade: int) -> None:
        if not 2 <= grade <= 5:
            raise ValueError("Grade must be in range 2..5")
        self._grades.append(grade)

    @property
    def average(self) -> float:
        return round(mean(self._grades), 2) if self._grades else 0.0

    def describe(self) -> str:
        return (
            f"Student {self.full_name} ({self.group}), "
            f"age {self.age}, avg grade {self.average}"
        )


class Teacher(Person):
    def __init__(self, full_name: str, age: int, subject: str) -> None:
        super().__init__(full_name, age)
        self.subject = subject

    def describe(self) -> str:
        return f"Teacher {self.full_name}, subject: {self.subject}"


@dataclass
class Group:
    name: str
    students: list[Student] = field(default_factory=list)
    curator: Teacher | None = None

    def add(self, student: Student) -> None:
        self.students.append(student)

    @property
    def average(self) -> float:
        if not self.students:
            return 0.0
        return round(mean(s.average for s in self.students), 2)

    def top_students(self, k: int = 3) -> list[Student]:
        return sorted(self.students, key=lambda s: s.average, reverse=True)[:k]


def main() -> int:
    group = Group(name="ИС-23-1")
    group.curator = Teacher("Иванова О.А.", 42, "Программирование")

    yudin = Student("Юдин Владислав", 18, group.name)
    yudin.add_grade(5)
    yudin.add_grade(4)
    yudin.add_grade(5)

    ivanov = Student("Иванов Иван", 19, group.name)
    ivanov.add_grade(4)
    ivanov.add_grade(3)

    petrov = Student("Петров Пётр", 18, group.name)
    petrov.add_grade(5)
    petrov.add_grade(5)
    petrov.add_grade(5)

    for s in (yudin, ivanov, petrov):
        group.add(s)

    print(f"Group: {group.name}")
    print(group.curator.describe() if group.curator else "(no curator)")
    print()
    for s in group.students:
        print("  - " + s.describe())
    print()
    print(f"Group average: {group.average}")
    print("Top 3:")
    for s in group.top_students():
        print(f"  * {s.full_name} — {s.average}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
