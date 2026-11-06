from genlib import *


def brute(n):
    if n <= 1:
        return 1
    return brute(n - 1) + brute(n - 2)


def fast(n):
    a, b = 1, 1
    for _ in range(n - 1):
        a, b = b, a + b
    return b


def samples():
    return [
        (lines(2), "2"),
        (lines(3), "3"),
    ]


def cases():
    for n in range(1, 21):
        assert brute(n) == fast(n)
    assert fast(45) == 1836311903
    return [lines(n) for n in (1, 4, 5, 10, 20, 30, 38, 40, 44, 45)]
