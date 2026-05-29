"""Лабораторная работа №3 (Python).

Тема: Работа в Tkinter.
Вариант: 1 (без вводимой части, формат ключа XXXXX-XXXXX-XXXXX).

Программа реализует простой keygen для абстрактного ПО:
- поле с сгенерированным ключом;
- кнопка генерации;
- кнопка копирования в буфер обмена;
- статусная строка.

Ключ состоит из латинских букв A-Z и цифр 0-9 в формате
XXXXX-XXXXX-XXXXX.

Запуск:
    python3 main.py
"""

from __future__ import annotations

import random
import string
import sys

ALPHABET = string.ascii_uppercase + string.digits


def generate_key() -> str:
    parts = ["".join(random.choices(ALPHABET, k=5)) for _ in range(3)]
    return "-".join(parts)


def main() -> int:
    try:
        import tkinter as tk
        from tkinter import ttk
    except Exception as exc:
        print(f"Tkinter is not available: {exc}", file=sys.stderr)
        print("Fallback (5 keys):")
        for _ in range(5):
            print("  " + generate_key())
        return 0

    window = tk.Tk()
    window.title("KeyGen — Lab 3")
    window.geometry("420x200")
    window.resizable(False, False)

    title = ttk.Label(window, text="License key generator", font=("Helvetica", 14, "bold"))
    title.pack(pady=(16, 8))

    key_var = tk.StringVar(value=generate_key())
    key_entry = ttk.Entry(window, textvariable=key_var, font=("Menlo", 14), justify="center", width=24)
    key_entry.pack(pady=4)

    status_var = tk.StringVar(value="Press 'Generate' to create a new key.")

    def regenerate() -> None:
        key_var.set(generate_key())
        status_var.set("New key generated.")

    def copy_to_clipboard() -> None:
        window.clipboard_clear()
        window.clipboard_append(key_var.get())
        status_var.set("Key copied to clipboard.")

    btns = ttk.Frame(window)
    btns.pack(pady=8)
    ttk.Button(btns, text="Generate", command=regenerate).grid(row=0, column=0, padx=6)
    ttk.Button(btns, text="Copy",     command=copy_to_clipboard).grid(row=0, column=1, padx=6)
    ttk.Button(btns, text="Quit",     command=window.destroy).grid(row=0, column=2, padx=6)

    status = ttk.Label(window, textvariable=status_var, foreground="#555")
    status.pack(side="bottom", pady=8)

    window.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
