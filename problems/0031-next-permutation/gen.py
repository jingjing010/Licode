from itertools import permutations

from genlib import *


def brute(a):
    """枚举所有不同排列，取字典序下一个（没有则取最小）"""
    ps = sorted(set(permutations(a)))
    k = ps.index(tuple(a))
    return list(ps[(k + 1) % len(ps)])


def fast(a):
    a = a[:]
    n = len(a)
    i = n - 2
    while i >= 0 and a[i] >= a[i + 1]:
        i -= 1
    if i >= 0:
        j = n - 1
        while a[j] <= a[i]:
            j -= 1
        a[i], a[j] = a[j], a[i]
    a[i + 1:] = a[i + 1:][::-1]
    return a


def samples():
    return [
        (lines(arr([1, 2, 3])), "[1,3,2]"),
        (lines(arr([3, 2, 1])), "[1,2,3]"),
        (lines(arr([1, 1, 5])), "[1,5,1]"),
    ]


def cases():
    for _ in range(400):
        a = rand_arr(random.randint(1, 7), 0, 3)
        assert brute(a) == fast(a)
    desc = sorted(rand_arr(100, 0, 100), reverse=True)
    return [
        lines(arr([5])),
        lines(arr([1, 2])),
        lines(arr([2, 1])),
        lines(arr([1, 1])),
        lines(arr([1, 3, 2])),
        lines(arr([2, 3, 1])),
        lines(arr([1, 5, 1])),
        lines(arr([2, 2, 0, 4, 3, 1])),
        lines(arr([1, 2, 3, 6, 5, 4])),
        lines(arr(rand_arr(10, 0, 5))),
        lines(arr([7] * 100)),
        lines(arr(desc)),
        lines(arr(list(range(100)))),
        lines(arr([50] + list(range(100, 51, -1)) + [51] + list(range(49, 0, -1)))),
        lines(arr(rand_arr(100, 0, 100))),
    ]
