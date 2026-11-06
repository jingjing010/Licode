from genlib import *


def brute(inp):
    """输入合法时，任何正确的解法都应输出 true"""
    return "true"


def samples():
    return [
        (lines(arr([-10, -3, 0, 5, 9])), "true"),
        (lines(arr([1, 3])), "true"),
    ]


def cases():
    res = [
        lines(arr([0])),
        lines(arr([-10000, 10000])),
        lines(arr([1, 2, 3])),
        lines(arr([1, 2, 3, 4])),
        lines(arr(range(1, 8))),
        lines(arr(range(1, 17))),
        lines(arr(range(-10000, 0))),
        lines(arr(range(-10000, 10000, 2))),
        lines(arr(range(1, 10001))),
    ]
    for n in (5, 6, 31, 100, 1023, 1024, 5000, 9999):
        res.append(lines(arr(sorted(rand_distinct(n, -10**4, 10**4)))))
    return res
