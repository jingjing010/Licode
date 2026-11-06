from genlib import *


def samples():
    return [
        (lines(arr([-2, 1, -3, 4, -1, 2, 1, -5, 4])), "6"),
        (lines(arr([1])), "1"),
        (lines(arr([5, 4, -1, 7, 8])), "23"),
    ]


def brute(text):
    """O(n^2) 暴力，用于对小数据交叉验证 solution.c 的输出"""
    nums = [int(x) for x in text.split("\n")[0].strip("[]").split(",")]
    best = nums[0]
    for i in range(len(nums)):
        t = 0
        for j in range(i, len(nums)):
            t += nums[j]
            best = max(best, t)
    return str(best)


def cases():
    res = [
        lines(arr([-5])),
        lines(arr([-3, -1, -2])),
        lines(arr([0, 0, 0])),
        lines(arr([10000] * 7)),
        lines(arr([-1, 10000, -10000, 10000, -1])),
    ]
    for n in (10, 50, 300):
        res.append(lines(arr(rand_arr(n, -100, 100))))
    res.append(lines(arr(rand_arr(10**5, -10**4, 10**4))))
    res.append(lines(arr(rand_arr(10**5, -10**4, -1))))
    res.append(lines(arr([10**4] * 10**5)))
    res.append(lines(arr(rand_arr(10**5, -10**4, 10**4 // 2))))
    return res
