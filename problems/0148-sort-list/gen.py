from genlib import *

V = 10**5
N = 5 * 10**4


def brute(inp):
    a = [int(x) for x in inp.split("\n")[0].strip("[]").split(",") if x]
    return arr(sorted(a))


def samples():
    res = [
        (lines(arr([4, 2, 1, 3])), "[1,2,3,4]"),
        (lines(arr([-1, 5, 3, 4, 0])), "[-1,0,3,4,5]"),
        (lines(arr([])), "[]"),
    ]
    for inp, want in res:
        assert brute(inp) == want
    return res


def cases():
    return [
        lines(arr([1])),
        lines(arr([2, 1])),
        lines(arr([3, 3, 3])),
        lines(arr([5, -5, 0, 5, -5])),
        lines(arr(rand_arr(10, -10, 10))),
        lines(arr(rand_arr(101, -V, V))),
        lines(arr(rand_arr(1000, -V, V))),
        lines(arr(rand_arr(N, -V, V))),
        lines(arr(list(range(-N // 2, N // 2)))),
        lines(arr(list(range(N // 2, -N // 2, -1)))),
        lines(arr([V] * N)),
        lines(arr(rand_arr(N, -3, 3))),
        lines(arr(rand_arr(N - 1, -V, V))),
        lines(arr([V if i % 2 else -V for i in range(N)])),
    ]
