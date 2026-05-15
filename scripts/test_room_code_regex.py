#!/usr/bin/env python3
"""Задание 10 — тест regex кода номера (как scripts/test_client_code_regex.py в MetLab12)."""

import re
import sys

ROOM_CODE_RE = re.compile(r"^[A-Z]{1,2}-\d{1,2}-\d{2,3}$")

VALID = ["AB-3-12", "A-1-05", "XY-12-999"]
INVALID = ["ab312", "AB-3", "123-45-67", ""]


def check(code: str) -> bool:
    return bool(ROOM_CODE_RE.match(code.strip().upper()))


def main() -> int:
    failed = 0
    for s in VALID:
        ok = check(s)
        print(f"  {s!r}: {'OK' if ok else 'FAIL'}")
        failed += not ok
    for s in INVALID:
        ok = check(s)
        print(f"  {s!r}: {'OK (expected fail)' if not ok else 'UNEXPECTED PASS'}")
        failed += ok
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
