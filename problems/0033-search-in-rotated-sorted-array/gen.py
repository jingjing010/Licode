from genlib import *

V = 10**4


def samples():
    return [
        (lines(arr([4, 5, 6, 7, 0, 1, 2]), 0), "4"),
        (lines(arr([4, 5, 6, 7, 0, 1, 2]), 3), "-1"),
        (lines(arr([1]), 0), "-1"),
    ]


def rotated(n, lo=-V, hi=V):
    a = sorted(rand_distinct(n, lo, hi))
    k = random.randrange(n)
    return a[k:] + a[:k]


def cases():
    res = [
        lines(arr([1]), 1),
        lines(arr([3, 1]), 1),
        lines(arr([3, 1]), 3),
        lines(arr([1, 3]), 3),
        lines(arr([5, 1, 3]), 5),
        lines(arr([5, 1, 3]), 3),
        lines(arr([4, 5, 6, 7, 8, 1, 2, 3]), 8),
        lines(arr([1, 2, 3, 4, 5]), 4),
        lines(arr([V, -V]), -V),
    ]
    for n in (10, 100, 1000):
        a = rotated(n)
        res.append(lines(arr(a), random.choice(a)))
        res.append(lines(arr(a), random.randint(-V, V)))
    a = rotated(5000)
    res.append(lines(arr(a), a[0]))
    res.append(lines(arr(a), a[-1]))
    res.append(lines(arr(a), random.choice(a)))
    present = set(a)
    t = next(x for x in range(-V, V + 1) if x not in present)
    res.append(lines(arr(a), t))
    return res
