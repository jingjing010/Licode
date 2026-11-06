from genlib import *
from collections import deque

V = 10**4


def samples():
    return [
        (lines(arr([1, 3, -1, -3, 5, 3, 6, 7]), 3), "[3,3,5,5,6,7]"),
        (lines(arr([1]), 1), "[1]"),
    ]


def brute(nums, k):
    return [max(nums[i:i + k]) for i in range(len(nums) - k + 1)]


def fast(nums, k):
    dq, res = deque(), []
    for i, x in enumerate(nums):
        while dq and nums[dq[-1]] <= x:
            dq.pop()
        dq.append(i)
        if dq[0] <= i - k:
            dq.popleft()
        if i >= k - 1:
            res.append(nums[dq[0]])
    return res


for _ in range(300):
    _a = rand_arr(random.randint(1, 15), -5, 5)
    _k = random.randint(1, len(_a))
    assert brute(_a, _k) == fast(_a, _k)


def cases():
    N = 10**5
    res = [
        lines(arr([-5]), 1),
        lines(arr([1, -1]), 1),
        lines(arr([1, -1]), 2),
        lines(arr([7, 2, 4]), 2),
        lines(arr([4, 4, 4, 4, 4]), 3),
        lines(arr([1, 2, 3, 4, 5, 6]), 4),
        lines(arr([6, 5, 4, 3, 2, 1]), 4),
        lines(arr([9, 10, 9, -7, -4, -8, 2, -6]), 5),
    ]
    res.append(lines(arr(rand_arr(50, -10, 10)), 7))
    res.append(lines(arr(rand_arr(1000, -V, V)), 30))
    res.append(lines(arr(rand_arr(N, -V, V)), 1))
    res.append(lines(arr(rand_arr(N, -V, V)), N))
    res.append(lines(arr(rand_arr(N, -V, V)), N // 2))
    res.append(lines(arr(rand_arr(N, -V, V)), 1000))
    # 递减序列：单调队列会一直变长；递增序列：每步都要清空队列
    res.append(lines(arr([V - i * 2 // 10 for i in range(N)]), 50000))
    res.append(lines(arr([-V + i * 2 // 10 for i in range(N)]), 50000))
    res.append(lines(arr(rand_arr(N, -3, 3)), 777))
    return res
