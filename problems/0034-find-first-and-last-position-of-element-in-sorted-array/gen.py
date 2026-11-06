from genlib import *

INF = 10**9


def samples():
    return [
        (lines(arr([5, 7, 7, 8, 8, 10]), 8), "[3,4]"),
        (lines(arr([5, 7, 7, 8, 8, 10]), 6), "[-1,-1]"),
        (lines(arr([]), 0), "[-1,-1]"),
    ]


def cases():
    res = [
        lines(arr([1]), 1),
        lines(arr([1]), 0),
        lines(arr([2, 2]), 2),
        lines(arr([1, 2, 3]), 3),
        lines(arr([-INF, -INF, INF, INF]), INF),
        lines(arr([-INF, -INF, INF, INF]), -INF),
        lines(arr([INF - 1]), INF),
    ]
    for n in (10, 100, 1000):
        a = rand_sorted(n, -20, 20)
        res.append(lines(arr(a), random.choice(a)))
        res.append(lines(arr(a), random.randint(-25, 25)))
    res.append(lines(arr([7] * 10**5), 7))
    a = rand_sorted(10**5, -INF, INF)
    res.append(lines(arr(a), a[12345]))
    a = rand_sorted(10**5, -1000, 1000)
    res.append(lines(arr(a), a[50000]))
    res.append(lines(arr(a), 1001))
    return res
