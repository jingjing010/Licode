from genlib import *

N = 10**5


def brute(t):
    out = []
    for i, x in enumerate(t):
        d = 0
        for j in range(i + 1, len(t)):
            if t[j] > x:
                d = j - i
                break
        out.append(d)
    return out


def samples():
    data = [
        ([73, 74, 75, 71, 69, 72, 76, 73], "[1,1,4,2,1,1,0,0]"),
        ([30, 40, 50, 60], "[1,1,1,0]"),
        ([30, 60, 90], "[1,1,0]"),
    ]
    for t, want in data:
        assert arr(brute(t)) == want
    return [(lines(arr(t)), want) for t, want in data]


def cases():
    res = [
        lines(arr([30])),
        lines(arr([100, 30])),
        lines(arr([50, 50, 50, 50])),
        lines(arr([90, 80, 70, 60, 100])),
        lines(arr([30, 100, 30, 100, 30])),
    ]
    for n in (20, 200, 2000):
        res.append(lines(arr(rand_arr(n, 30, 100))))
    res.append(lines(arr(rand_arr(N, 30, 100))))
    res.append(lines(arr([100 - i * 70 // N for i in range(N)])))
    res.append(lines(arr([30 + i * 70 // N for i in range(N)])))
    res.append(lines(arr([70] * (N - 1) + [100])))
    res.append(lines(arr([100 - (i % 71) for i in range(N)])))
    return res
