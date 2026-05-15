#!/usr/bin/env python3
"""Задание 10: тест регулярного выражения кода номера отеля."""

import re
import sys

# 1–2 буквы корпуса, этаж 1–2 цифры, номер 2–3 цифры
ROOM_CODE_RE = re.compile(r"^[A-Z]{1,2}-\d{1,2}-\d{2,3}$")

VALID = ["AB-3-12", "A-1-05", "XY-12-999", "B-2-10"]
INVALID = ["ab312", "AB-3", "123-45-67", "AB-3-1234", "", "AB-3-1"]


def check(code: str) -> bool:
    return bool(ROOM_CODE_RE.match(code.strip().upper()))


def main() -> int:
    failed = 0
    print("=== Валидные примеры ===")
    for s in VALID:
        ok = check(s)
        print(f"  {s!r}: {'OK' if ok else 'FAIL'}")
        if not ok:
            failed += 1
    print("=== Невалидные примеры ===")
    for s in INVALID:
        ok = check(s)
        print(f"  {s!r}: {'OK (expected fail)' if not ok else 'UNEXPECTED PASS'}")
        if ok:
            failed += 1
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
