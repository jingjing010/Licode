from genlib import *

V = 10**9


def samples():
    return [
        (lines(arr([100, 4, 200, 1, 3, 2])), "4"),
        (lines(arr([0, 3, 7, 2, 5, 8, 4, 6, 0, 1])), "9"),
        (lines(arr([1, 0, 1, 2])), "3"),
    ]


def brute(nums):
    st = set(nums)
    best = 0
    for x in st:
        y = x
        while y in st:
            y += 1
        best = max(best, y - x)
    return best


def fast(nums):
    a = sorted(set(nums))
    best, cur = 0, 0
    for i, x in enumerate(a):
        cur = cur + 1 if i and a[i - 1] == x - 1 else 1
        best = max(best, cur)
    return best


for _ in range(300):
    _a = rand_arr(random.randint(0, 15), -10, 10)
    assert brute(_a) == fast(_a)


def runs(n, lo, hi, maxrun):
    """若干段随机长度的连续区间，加重复后打乱"""
    a = []
    while len(a) < n:
        start = random.randint(lo, hi)
        ln = random.randint(1, maxrun)
        a.extend(range(start, min(hi, start + ln - 1) + 1))
    a = a[:n]
    for i in random.sample(range(n), n // 10):
        a[i] = random.choice(a)
    random.shuffle(a)
    return a


def cases():
    N = 10**5
    res = [
        lines(arr([])),
        lines(arr([5])),
        lines(arr([7, 7, 7, 7])),
        lines(arr([-V, V])),
        lines(arr([V - 2, V, V - 1, -V, -V + 1])),
        lines(arr([9, 1, 4, 7, 3, -1, 0, 5, 8, -1, 6])),
        lines(arr([1, 3, 5, 7, 9])),
    ]
    res.append(lines(arr(rand_arr(30, -15, 15))))
    res.append(lines(arr(runs(1000, -2000, 2000, 30))))
    res.append(lines(arr(rand_arr(N, -V, V))))
    res.append(lines(arr(rand_arr(N, -60000, 60000))))
    res.append(lines(arr(runs(N, -V, V, 5000))))
    big = list(range(-V, -V + N))
    random.shuffle(big)
    res.append(lines(arr(big)))
    res.append(lines(arr([random.randint(0, 50) for _ in range(N)])))
    desc = list(range(V, V - N, -1))
    res.append(lines(arr(desc)))
    return res
