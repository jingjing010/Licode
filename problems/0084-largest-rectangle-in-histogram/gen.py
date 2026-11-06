from genlib import *

N = 10**5
H = 10**4


def brute(h):
    best = 0
    for i in range(len(h)):
        lo = h[i]
        for j in range(i, len(h)):
            lo = min(lo, h[j])
            best = max(best, lo * (j - i + 1))
    return best


def samples():
    assert brute([2, 1, 5, 6, 2, 3]) == 10
    assert brute([2, 4]) == 4
    return [
        (lines(arr([2, 1, 5, 6, 2, 3])), "10"),
        (lines(arr([2, 4])), "4"),
    ]


def cases():
    res = [
        lines(arr([0])),
        lines(arr([7])),
        lines(arr([0, 0, 0])),
        lines(arr([3, 3, 3, 3])),
        lines(arr([1, 2, 3, 4, 5])),
        lines(arr([5, 4, 3, 2, 1])),
        lines(arr([2, 0, 2])),
        lines(arr([4, 2, 0, 3, 2, 5])),
        lines(arr([1, 10000, 1])),
    ]
    for n, hi in ((10, 10), (100, 100), (1000, H)):
        res.append(lines(arr(rand_arr(n, 0, hi))))
    res.append(lines(arr([H] * N)))
    res.append(lines(arr([i % (H + 1) for i in range(N)])))
    res.append(lines(arr([H - i * H // N for i in range(N)])))
    res.append(lines(arr(rand_arr(N, 0, H))))
    res.append(lines(arr(rand_arr(N, 9000, H))))
    res.append(lines(arr([0 if i % 1000 == 0 else H for i in range(N)])))
    return res
