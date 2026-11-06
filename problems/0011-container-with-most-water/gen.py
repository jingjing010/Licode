from genlib import *


def samples():
    return [
        (lines(arr([1, 8, 6, 2, 5, 4, 8, 3, 7])), "49"),
        (lines(arr([1, 1])), "1"),
    ]


def brute(h):
    n = len(h)
    return max((j - i) * min(h[i], h[j]) for i in range(n) for j in range(i + 1, n))


def fast(h):
    l, r, best = 0, len(h) - 1, 0
    while l < r:
        best = max(best, (r - l) * min(h[l], h[r]))
        if h[l] < h[r]:
            l += 1
        else:
            r -= 1
    return best


for _ in range(300):
    _h = rand_arr(random.randint(2, 30), 0, 20)
    assert brute(_h) == fast(_h)


def cases():
    res = [
        lines(arr([0, 0])),
        lines(arr([4, 3, 2, 1, 4])),
        lines(arr([1, 2, 1])),
        lines(arr([2, 3, 4, 5, 18, 17, 6])),
        lines(arr([10000, 0, 0, 10000])),
    ]
    for n in (10, 100, 1000):
        res.append(lines(arr(rand_arr(n, 0, 10**4))))
    res.append(lines(arr(rand_arr(10**5, 0, 10**4))))
    res.append(lines(arr([10**4] * 10**5)))
    res.append(lines(arr([i % 10001 for i in range(10**5)])))
    res.append(lines(arr([0] * 10**5)))
    mountain = [min(i, 10**5 - 1 - i) // 5 for i in range(10**5)]
    res.append(lines(arr(mountain)))
    return res
