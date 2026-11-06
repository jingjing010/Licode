from genlib import *


def samples():
    return [
        (lines(arr([1, 2, 2, 3])), "true"),
        (lines(arr([6, 5, 4, 4])), "true"),
        (lines(arr([1, 3, 2])), "false"),
    ]


def cases():
    n = 10**5
    inc = rand_sorted(n, -10**5, 10**5)
    dec = inc[::-1]
    bad_end = inc[:]
    bad_end[-1] = bad_end[-2] - 1
    bad_mid = dec[:]
    bad_mid[n // 2] = bad_mid[n // 2 - 1] + 1
    return [
        lines(arr([5])),
        lines(arr([1, 1])),
        lines(arr([2, 1])),
        lines(arr([1, 1, 1, 2, 1])),
        lines(arr([3, 3, 2, 2, 1, 1])),
        lines(arr([1, 2, 4, 5, 3])),
        lines(arr(rand_arr(10, -3, 3))),
        lines(arr(rand_sorted(1000, -10, 10))),
        lines(arr(inc)),
        lines(arr(dec)),
        lines(arr(bad_end)),
        lines(arr(bad_mid)),
        lines(arr([-10**5] * n)),
        lines(arr(rand_arr(n, -10**5, 10**5))),
    ]
