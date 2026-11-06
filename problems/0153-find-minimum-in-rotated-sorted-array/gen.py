from genlib import *


def samples():
    return [
        (lines(arr([3, 4, 5, 1, 2])), "1"),
        (lines(arr([4, 5, 6, 7, 0, 1, 2])), "0"),
        (lines(arr([11, 13, 15, 17])), "11"),
    ]


def rotated(n, k=None):
    a = sorted(rand_distinct(n, -5000, 5000))
    if k is None:
        k = random.randrange(n)
    return a[k:] + a[:k]


def cases():
    res = [
        lines(arr([1])),
        lines(arr([2, 1])),
        lines(arr([1, 2])),
        lines(arr([5, 1, 2, 3, 4])),
        lines(arr([2, 3, 4, 5, 1])),
    ]
    for n in (10, 100, 1000):
        res.append(lines(arr(rotated(n))))
    res.append(lines(arr(rotated(5000, 0))))
    res.append(lines(arr(rotated(5000, 1))))
    res.append(lines(arr(rotated(5000, 4999))))
    res.append(lines(arr(rotated(5000))))
    res.append(lines(arr(rotated(5000))))
    return res
