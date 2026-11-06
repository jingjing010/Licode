from collections import Counter

from genlib import *

N = 10**5
V = 10**4


def brute(a, k):
    """答案唯一时返回排序后的前 k 高频元素，否则返回 None"""
    freq = sorted(Counter(a).items(), key=lambda t: -t[1])
    if k < len(freq) and freq[k - 1][1] == freq[k][1]:
        return None
    return sorted(v for v, _ in freq[:k])


def samples():
    data = [
        ([1, 1, 1, 2, 2, 3], 2, "[1,2]"),
        ([1], 1, "[1]"),
        ([1, 2, 1, 2, 1, 2, 3, 1, 3, 2], 2, "[1,2]"),
    ]
    for a, k, want in data:
        assert arr(brute(a, k)) == want
    return [(lines(arr(a), k), want) for a, k, want in data]


def unique_case(n, lo, hi):
    """随机数组 + 随机 k，保证前 k 高频集合唯一"""
    while True:
        a = rand_arr(n, lo, hi)
        d = len(set(a))
        ks = [k for k in range(1, d + 1) if brute(a, k) is not None]
        if ks:
            return lines(arr(a), random.choice(ks))


def build(freqs, lo=-V, hi=V):
    """给定每个不同数的出现次数，随机挑数值并打乱"""
    vals = rand_distinct(len(freqs), lo, hi)
    a = []
    for v, c in zip(vals, freqs):
        a += [v] * c
    random.shuffle(a)
    return a


def checked(a, k):
    assert brute(a, k) is not None and len(a) <= N
    return lines(arr(a), k)


def cases():
    res = [
        checked([-V], 1),
        checked([V, V, -V], 1),
        checked([5, 5, 5, 5], 1),
        checked([1, 2, 3, 4], 4),
        checked([4, 4, 4, -1, -1, 2], 3),
        checked([0, 0, 1, 1, 1, 2, 2, 2, 2], 2),
    ]
    for n, span in ((20, 5), (200, 30), (2000, 300)):
        res.append(unique_case(n, -span, span))
    res.append(checked(build([N // 2, N // 4] + [1] * (N // 4)), 2))
    res.append(checked(build(list(range(1, 447))), 100))
    res.append(checked(build(list(range(1, 447))), 446))
    res.append(checked(build([3] + [2] * 20000), 1))
    res.append(checked(build([5] * 1000 + [1] * 19001), 1000))
    res.append(checked(build([10] * 9000 + [1] * 10000), 9000))
    return res
