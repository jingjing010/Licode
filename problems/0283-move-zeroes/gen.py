from genlib import *

INT_MIN, INT_MAX = -2**31, 2**31 - 1


def samples():
    return [
        (lines(arr([0, 1, 0, 3, 12])), "[1,3,12,0,0]"),
        (lines(arr([0])), "[0]"),
    ]


def with_zeros(n, ratio, lo=INT_MIN, hi=INT_MAX):
    return [0 if random.random() < ratio else random.randint(lo, hi) for _ in range(n)]


def brute(a):
    nz = [x for x in a if x != 0]
    return nz + [0] * (len(a) - len(nz))


def cases():
    res = [
        lines(arr([1])),
        lines(arr([0, 0, 0, 0])),
        lines(arr([1, 2, 3, 4])),
        lines(arr([4, 2, 4, 0, 0, 3, 0, 5, 1, 0])),
        lines(arr([INT_MIN, 0, INT_MAX, 0])),
        lines(arr([0, 0, 0, 7])),
        lines(arr([-1, 0, -2, 0, -3])),
    ]
    for n in (10, 50, 300):
        res.append(lines(arr(with_zeros(n, 0.4, -10, 10))))
    res.append(lines(arr(with_zeros(10**4, 0.5))))
    res.append(lines(arr(with_zeros(10**4, 0.05))))
    res.append(lines(arr([0] * 9999 + [1])))
    res.append(lines(arr([5] + [0] * 9999)))
    return res
