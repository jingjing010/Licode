from genlib import *

V = 10**5
N = 3 * 10**4


def make(pa, pb, common):
    """A = pa + common，B = pb + common"""
    a, bb = pa + common, pb + common
    iv = common[0] if common else 0
    return lines(iv, arr(a), arr(bb), len(pa), len(pb))


def brute(inp):
    ls = inp.split("\n")
    skip_a = int(ls[3])
    a = [int(x) for x in ls[1].strip("[]").split(",")]
    return "Intersected at '%d'" % a[skip_a] if skip_a < len(a) else "No intersection"


def rnd(n):
    return rand_arr(n, 1, V)


def samples():
    res = [
        (make([4, 1], [5, 6, 1], [8, 4, 5]), "Intersected at '8'"),
        (make([1, 9, 1], [3], [2, 4]), "Intersected at '2'"),
        (make([2, 6, 4], [1, 5], []), "No intersection"),
    ]
    for inp, want in res:
        assert brute(inp) == want
    return res


def cases():
    return [
        make([], [], [1]),
        make([1], [2], []),
        make([], [7], [3, 4]),
        make([7], [], [3, 4]),
        make([1, 1], [1, 1, 1], [1, 1]),
        make(rnd(5), rnd(9), rnd(1)),
        make(rnd(30), rnd(3), rnd(40)),
        make(rnd(100), rnd(200), []),
        make(rnd(1000), rnd(10), rnd(500)),
        make([], [], rnd(N)),
        make(rnd(N - 1), [], rnd(1)),
        make(rnd(N), rnd(N), []),
        make(rnd(N // 2), rnd(N - 1), rnd(1)),
        make(rnd(1), rnd(N // 2), rnd(N // 2)),
        make([5] * (N // 2), [5] * (N // 3), [5] * (N // 2)),
    ]
