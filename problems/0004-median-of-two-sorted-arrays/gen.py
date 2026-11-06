from genlib import *

V = 10**6


def samples():
    return [
        (lines(arr([1, 3]), arr([2])), "2.00000"),
        (lines(arr([1, 2]), arr([3, 4])), "2.50000"),
    ]


def brute(a, b):
    c = sorted(a + b)
    k = len(c)
    if k % 2:
        return "%.5f" % c[k // 2]
    return "%.5f" % ((c[k // 2 - 1] + c[k // 2]) / 2)


for _a, _b, _want in (([1, 3], [2], "2.00000"), ([1, 2], [3, 4], "2.50000"), ([], [-1, 0], "-0.50000")):
    assert brute(_a, _b) == _want


def case(a, b):
    return lines(arr(a), arr(b))


def cases():
    res = [
        case([], [1]),
        case([2], []),
        case([], [2, 3]),
        case([1, 1, 1], [1, 1]),
        case([1, 2], [-1, 3]),
        case([-V, -V], [V]),
        case([V, V], [V, V]),
        case([-V], [-V + 1]),
        case(list(range(1, 6)), list(range(6, 11))),
    ]
    for (m, n) in ((5, 7), (30, 1), (0, 1000), (1000, 0), (1, 999)):
        res.append(case(rand_sorted(m, -100, 100), rand_sorted(n, -100, 100)))
    res.append(case(rand_sorted(1000, -V, V), rand_sorted(1000, -V, V)))
    res.append(case(rand_sorted(1000, -V, 0), rand_sorted(999, 0, V)))
    return res
