from genlib import *


def samples():
    return [
        (lines(arr([1, 1, 1]), 2), "2"),
        (lines(arr([1, 2, 3]), 3), "2"),
    ]


def brute(nums, k):
    cnt = 0
    for i in range(len(nums)):
        t = 0
        for j in range(i, len(nums)):
            t += nums[j]
            cnt += t == k
    return cnt


def fast(nums, k):
    seen, pre, cnt = {0: 1}, 0, 0
    for x in nums:
        pre += x
        cnt += seen.get(pre - k, 0)
        seen[pre] = seen.get(pre, 0) + 1
    return cnt


for _ in range(300):
    _a = rand_arr(random.randint(1, 15), -3, 3)
    _k = random.randint(-4, 4)
    assert brute(_a, _k) == fast(_a, _k)


def cases():
    N = 2 * 10**4
    res = [
        lines(arr([1]), 1),
        lines(arr([1]), 0),
        lines(arr([0]), 0),
        lines(arr([-1, -1, 1]), 0),
        lines(arr([1, -1, 0]), 0),
        lines(arr([1000] * 5), 10**7),
        lines(arr([3, 4, 7, 2, -3, 1, 4, 2]), 7),
        lines(arr([-1000, 1000] * 5), 0),
    ]
    res.append(lines(arr(rand_arr(50, -5, 5)), 3))
    res.append(lines(arr(rand_arr(1000, -10, 10)), -7))
    # 全 0、k = 0：答案 n(n+1)/2 = 200010000，接近 int 上限
    res.append(lines(arr([0] * N), 0))
    res.append(lines(arr(rand_arr(N, -1000, 1000)), 0))
    res.append(lines(arr(rand_arr(N, -1000, 1000)), 1234))
    res.append(lines(arr(rand_arr(N, -3, 3)), 2))
    res.append(lines(arr([1000] * N), 10**7))
    res.append(lines(arr([-1000] * N), -10**7))
    res.append(lines(arr(rand_arr(N, 0, 1000)), 10**7))
    res.append(lines(arr(rand_arr(N, -1000, 1000)), -10**7))
    return res
