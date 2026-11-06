from genlib import *


def samples():
    return [
        (lines(arr([2, 7, 11, 15]), 9), "[0,1]"),
        (lines(arr([3, 2, 4]), 6), "[1,2]"),
        (lines(arr([3, 3]), 6), "[0,1]"),
    ]


def unique_pair_case(n, lo, hi):
    """随机数组 + 保证恰好只有一对下标的和等于 target"""
    while True:
        nums = rand_distinct(n, lo, hi)
        i, j = random.sample(range(n), 2)
        target = nums[i] + nums[j]
        seen, cnt = {}, 0
        for x in nums:
            cnt += seen.get(target - x, 0)
            seen[x] = seen.get(x, 0) + 1
        if cnt == 1:
            return lines(arr(nums), target)


def cases():
    res = [
        lines(arr([0, 4, 3, 0]), 0),
        lines(arr([-1, -2, -3, -4, -5]), -8),
        lines(arr([1000000000, -1000000000, 5]), 0),
    ]
    for n in (10, 100, 1000):
        res.append(unique_pair_case(n, -5 * 10**8, 5 * 10**8))
    for _ in range(2):
        res.append(unique_pair_case(10**4, -10**9 // 2, 10**9 // 2))
    return res
