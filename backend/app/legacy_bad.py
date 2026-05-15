"""
Задание 3: намеренно «плохая» функция (до рефакторинга).
См. app/services/stay_charges.py и docs/assignment03_refactoring.md
"""


def calc(x, y, z, a, b, c, d, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w):
    # магические числа, дублирование, нет обработки ошибок
    if x > 7:
        t1 = z * 0.9
    else:
        t1 = z
    if a == 1:
        t1 = t1 * 0.95
    if b == 1:
        t1 = t1 * 0.95
    if y > 2:
        t1 = t1 + 500 * (y - 2)
    if c == 1:
        t1 = t1 + z * 0.15
    if d == 1:
        t1 = t1 + z * 0.15
    if f == 1:
        t1 = t1 - z * 0.1
    if g == 1:
        t1 = t1 - z * 0.05
    if h == 1:
        t1 = t1 - z * 0.05
    if i == 1:
        t1 = t1 + 100
    if j == 1:
        t1 = t1 + 200
    if k == 1:
        t1 = t1 + 300
    if l == 1:
        t1 = t1 + 400
    if m == 1:
        t1 = t1 + 500
    if n == 1:
        t1 = t1 + 600
    if o == 1:
        t1 = t1 + 700
    if p == 1:
        t1 = t1 + 800
    if q == 1:
        t1 = t1 + 900
    if r == 1:
        t1 = t1 + 1000
    if s == 1:
        t1 = t1 + 1100
    if t == 1:
        t1 = t1 + 1200
    if u == 1:
        t1 = t1 + 1300
    if v == 1:
        t1 = t1 + 1400
    if w == 1:
        t1 = t1 + 1500
    return round(t1, 2)
