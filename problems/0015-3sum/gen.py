from genlib import *
from itertools import combinations

V = 10**5


def samples():
    return [
        (lines(arr([-1, 0, 1, 2, -1, -4])), "[[-1,-1,2],[-1,0,1]]"),
        (lines(arr([0, 1, 1])), "[]"),
        (lines(arr([0, 0, 0])), "[[0,0,0]]"),
    ]


def brute(nums):
    return sorted({tuple(sorted(t)) for t in combinations(nums, 3) if sum(t) == 0})


def fast(nums):
    a, n, res = sorted(nums), len(nums), set()
    for i in range(n - 2):
        l, r = i + 1, n - 1
        while l < r:
            t = a[i] + a[l] + a[r]
            if t < 0:
                l += 1
            elif t > 0:
                r -= 1
            else:
                res.add((a[i], a[l], a[r]))
                l += 1
                r -= 1
    return sorted(res)


for _ in range(300):
    _a = rand_arr(random.randint(3, 12), -6, 6)
    assert brute(_a) == fast(_a)


def checked(nums):
    """输出不能超过 1MB"""
    out = mat(fast(nums))
    assert len(out) < 900000, len(out)
    return lines(arr(nums))


def cases():
    N = 3000
    res = [
        checked([0, 0, 0, 0]),
        checked([1, 2, 3]),
        checked([-1, -2, -3]),
        checked([-2, 0, 1, 1, 2]),
        checked([3, 0, -2, -1, 1, 2]),
        checked([-V, 0, V, V // 2, V // 2, -V // 2, -V // 2]),
        checked([-4, -2, -2, -2, 0, 1, 2, 2, 2, 3, 3, 4, 4, 6, 6]),
    ]
    res.append(checked(rand_arr(30, -10, 10)))
    res.append(checked(rand_arr(300, -100, 100)))
    res.append(checked(rand_arr(N, -V, V)))
    res.append(checked(rand_arr(N, -V, V)))
    res.append(checked(rand_arr(N, -200, 200)))
    res.append(checked(rand_arr(N, -5, 5)))
    res.append(checked([0] * N))
    res.append(checked(rand_arr(N, 1, V)))
    res.append(checked(rand_distinct(N, -V, V)))
    return res
