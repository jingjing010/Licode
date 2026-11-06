from genlib import *

INT_MIN, INT_MAX = -2**31, 2**31 - 1


def samples():
    return [
        (lines(arr([1, 2, 3, 4, 5, 6, 7]), 3), "[5,6,7,1,2,3,4]"),
        (lines(arr([-1, -100, 3, 99]), 2), "[3,99,-1,-100]"),
    ]


def brute(nums, k):
    a = list(nums)
    for _ in range(k % len(a)):
        a = [a[-1]] + a[:-1]
    return a


def fast(nums, k):
    n = len(nums)
    return [nums[(i - k) % n] for i in range(n)]


for _ in range(300):
    _a = rand_arr(random.randint(1, 12), -50, 50)
    _k = random.randint(0, 40)
    assert brute(_a, _k) == fast(_a, _k)


def cases():
    N = 10**5
    res = [
        lines(arr([1]), 0),
        lines(arr([1]), 100000),
        lines(arr([1, 2]), 1),
        lines(arr([1, 2]), 2),
        lines(arr([1, 2, 3]), 4),
        lines(arr([1, 2, 3, 4, 5, 6]), 6),
        lines(arr([1, 2, 3, 4, 5, 6]), 0),
        lines(arr([1, 2, 3, 4, 5, 6]), 5),
        lines(arr([INT_MIN, INT_MAX, 0, -1]), 3),
    ]
    for n in (10, 100, 1000):
        res.append(lines(arr(rand_arr(n, INT_MIN, INT_MAX)), random.randint(0, 3 * n)))
    # 最大规模（输出上限 1MB，数值控制在 6 位以内）
    res.append(lines(arr(rand_arr(N, -99999, 99999)), 100000))
    res.append(lines(arr(rand_arr(N, -99999, 99999)), 99999))
    res.append(lines(arr(rand_arr(N - 7, -99999, 99999)), 100000))
    res.append(lines(arr(rand_arr(N, -99999, 99999)), 37))
    return res
