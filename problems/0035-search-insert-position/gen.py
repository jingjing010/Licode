from genlib import *


def samples():
    return [
        (lines(arr([1, 3, 5, 6]), 5), "2"),
        (lines(arr([1, 3, 5, 6]), 2), "1"),
        (lines(arr([1, 3, 5, 6]), 7), "4"),
    ]


def sorted_distinct(n, lo=-10**4, hi=10**4):
    return sorted(rand_distinct(n, lo, hi))


def cases():
    res = [
        lines(arr([1]), 0),
        lines(arr([1]), 1),
        lines(arr([1]), 2),
        lines(arr([-10000, 10000]), -10000),
        lines(arr([-10000, 10000]), 10000),
        lines(arr([-10000, 10000]), 0),
    ]
    for n in (10, 100, 1000):
        a = sorted_distinct(n)
        res.append(lines(arr(a), random.choice(a)))
        res.append(lines(arr(a), random.randint(-10**4, 10**4)))
    a = sorted_distinct(10**4)
    res.append(lines(arr(a), random.choice(a)))
    res.append(lines(arr(a), -10**4 if a[0] != -10**4 else 10**4))
    res.append(lines(arr(list(range(-5000, 5000))), 5000))
    return res
