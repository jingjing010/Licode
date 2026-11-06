import json

from genlib import *


def brute(inp):
    ls = inp.split("\n")
    a = json.loads(ls[0])
    pos = int(ls[1])
    return str(pos if a else -1)


def case(n, pos):
    return lines(arr(rand_arr(n, -10**5, 10**5)), pos)


def samples():
    res = [
        (lines(arr([3, 2, 0, -4]), 1), "1"),
        (lines(arr([1, 2]), 0), "0"),
        (lines(arr([1]), -1), "-1"),
    ]
    for inp, want in res:
        assert brute(inp) == want
    return res


def cases():
    N = 10**4
    res = [
        lines(arr([]), -1),
        lines(arr([1]), 0),
        lines(arr([1, 2]), -1),
        lines(arr([1, 2]), 1),
        case(3, 1),
        case(10, 9),
        case(10, -1),
        case(100, 37),
        case(1000, -1),
        case(N, 0),
        case(N, N - 1),
        case(N, -1),
        case(N, random.randrange(N)),
        case(N, 1),
        lines(arr([5] * N), N // 2),
    ]
    return res
