from itertools import product

from genlib import *


def brute(a):
    """枚举所有不相邻的偷法"""
    best = 0
    for pick in product((0, 1), repeat=len(a)):
        if any(pick[i] and pick[i + 1] for i in range(len(a) - 1)):
            continue
        best = max(best, sum(x for x, p in zip(a, pick) if p))
    return best


def fast(a):
    p2 = p1 = 0
    for x in a:
        p2, p1 = p1, max(p1, p2 + x)
    return p1


def samples():
    return [
        (lines(arr([1, 2, 3, 1])), "4"),
        (lines(arr([2, 7, 9, 3, 1])), "12"),
    ]


def cases():
    for _ in range(300):
        a = rand_arr(random.randint(1, 12), 0, 20)
        assert brute(a) == fast(a)
    return [
        lines(arr([0])),
        lines(arr([400])),
        lines(arr([1, 2])),
        lines(arr([2, 1])),
        lines(arr([2, 1, 1, 2])),
        lines(arr([0, 0, 0, 0])),
        lines(arr([5, 1, 1, 5, 1, 1, 5])),
        lines(arr(rand_arr(10, 0, 400))),
        lines(arr(rand_arr(50, 0, 400))),
        lines(arr([400] * 100)),
        lines(arr([0, 400] * 50)),
        lines(arr(rand_arr(100, 0, 400))),
        lines(arr(rand_arr(100, 300, 400))),
        lines(arr(rand_arr(99, 0, 3))),
    ]
