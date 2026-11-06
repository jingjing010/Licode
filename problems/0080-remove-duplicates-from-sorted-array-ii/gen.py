from collections import Counter

from genlib import *

N = 3 * 10**4


def brute(a):
    cnt = Counter()
    kept = []
    for x in a:
        cnt[x] += 1
        if cnt[x] <= 2:
            kept.append(x)
    return "%d\n%s" % (len(kept), arr(kept))


def fast(a):
    a = list(a)
    k = 0
    for x in a:
        if k < 2 or x != a[k - 2]:
            a[k] = x
            k += 1
    return "%d\n%s" % (k, arr(a[:k]))


def samples():
    res = []
    for a, want in (([1, 1, 1, 2, 2, 3], "5\n[1,1,2,2,3]"),
                    ([0, 0, 1, 1, 1, 1, 2, 3, 3], "7\n[0,0,1,1,2,3,3]")):
        assert brute(a) == want
        res.append((lines(arr(a)), want))
    return res


def cases():
    for _ in range(300):
        a = rand_sorted(random.randint(1, 12), -3, 3)
        assert brute(a) == fast(a)
    res = [
        lines(arr([1])),
        lines(arr([1, 1])),
        lines(arr([1, 2])),
        lines(arr([5, 5, 5])),
        lines(arr([-1, 0, 0, 0, 0, 3, 3])),
        lines(arr([1, 2, 3, 4, 5, 6])),
        lines(arr([-10**4, -10**4, -10**4, 10**4, 10**4, 10**4])),
        lines(arr([7] * N)),
        lines(arr(list(range(-15000, 15000)))),
        lines(arr([v for v in range(-5000, 5000) for _ in range(3)])),
    ]
    for n, lo, hi in ((10, -2, 2), (50, -5, 5), (1000, -100, 100)):
        res.append(lines(arr(rand_sorted(n, lo, hi))))
    res.append(lines(arr(rand_sorted(N, -10**4, 10**4))))
    res.append(lines(arr(rand_sorted(N, -100, 100))))
    return res
