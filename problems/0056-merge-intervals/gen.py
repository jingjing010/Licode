from genlib import *
import json


def samples():
    return [
        (lines(mat([[1, 3], [2, 6], [8, 10], [15, 18]])), "[[1,6],[8,10],[15,18]]"),
        (lines(mat([[1, 4], [4, 5]])), "[[1,5]]"),
        (lines(mat([[4, 7], [1, 4]])), "[[1,7]]"),
    ]


def brute(text):
    """在数轴上逐点标记覆盖（坐标乘 2，区分「相接」和「相离」），再找连续段"""
    iv = json.loads(text.split("\n")[0])
    cov = [False] * (2 * 10**4 + 3)
    for l, r in iv:
        for x in range(2 * l, 2 * r + 1):
            cov[x] = True
    res, x = [], 0
    while x < len(cov):
        if cov[x]:
            y = x
            while cov[y + 1]:
                y += 1
            res.append([x // 2, y // 2])
            x = y + 1
        else:
            x += 1
    return mat(res)


def rand_intervals(n, hi, maxlen):
    res = []
    for _ in range(n):
        l = random.randint(0, hi)
        r = min(hi, l + random.randint(0, maxlen))
        res.append([l, r])
    return res


def fast(iv):
    res = []
    for l, r in sorted(iv):
        if res and l <= res[-1][1]:
            res[-1][1] = max(res[-1][1], r)
        else:
            res.append([l, r])
    return mat(res)


for _ in range(200):
    _iv = rand_intervals(random.randint(1, 8), 30, 6)
    assert brute(lines(mat(_iv))) == fast(_iv)


def cases():
    res = [
        lines(mat([[0, 0]])),
        lines(mat([[1, 4], [0, 4]])),
        lines(mat([[1, 4], [2, 3]])),
        lines(mat([[1, 1], [2, 2], [3, 3]])),
        lines(mat([[5, 5], [5, 5], [5, 5]])),
        lines(mat([[2, 3], [4, 5], [6, 7], [8, 9], [1, 10]])),
        lines(mat([[0, 10000], [10000, 10000], [0, 0]])),
    ]
    for n, hi, ml in ((5, 20, 3), (20, 100, 5), (100, 1000, 20)):
        res.append(lines(mat(rand_intervals(n, hi, ml))))
    res.append(lines(mat(rand_intervals(10**4, 10**4, 0))))
    res.append(lines(mat(rand_intervals(10**4, 10**4, 3))))
    res.append(lines(mat(rand_intervals(10**4, 10**4, 10**4))))
    big = [[i, i] for i in range(0, 10**4 + 1, 2)]
    random.shuffle(big)
    res.append(lines(mat(big)))
    return res
