from genlib import *


def samples():
    return [
        (lines(arr([1, 2, 3, 4])), "[24,12,8,6]"),
        (lines(arr([-1, 1, 0, -3, 3])), "[0,0,9,0,0]"),
    ]


def brute(text):
    nums = [int(x) for x in text.split("\n")[0].strip("[]").split(",")]
    res = []
    for i in range(len(nums)):
        p = 1
        for j, x in enumerate(nums):
            if j != i:
                p *= x
        res.append(p)
    return arr(res)


def safe_arr(n, budget, zeros=0):
    """非零元素绝对值的乘积 <= budget，保证任意前缀/后缀积都在 32 位范围内"""
    a = [random.choice((-1, 1)) for _ in range(n)]
    prod = 1
    for _ in range(4 * n):
        v = random.randint(2, 30)
        if prod * v > budget:
            continue
        prod *= v
        a[random.randrange(n)] = v * random.choice((-1, 1))
        if random.random() < 0.05:
            break
    # 被覆盖的位置可能把预算算多了，重新校验
    p = 1
    for x in a:
        p *= abs(x)
    assert p <= budget
    for i in random.sample(range(n), zeros):
        a[i] = 0
    return a


def cases():
    res = [
        lines(arr([0, 0])),
        lines(arr([0, 5])),
        lines(arr([-30, 30])),
        lines(arr([1, 1, 1, 1])),
        lines(arr([2, 3, 0, 4, 0])),
        lines(arr([-2, -3, -5, -7, 11])),
        lines(arr([30, 30, 30, 30, 30, 30])),
        lines(arr([-1, -1, -1, -1, -1, -1, 2])),
    ]
    for n in (10, 30, 200):
        res.append(lines(arr(safe_arr(n, 2**31 - 1))))
    res.append(lines(arr(safe_arr(50, 2**31 - 1, zeros=1))))
    # 最大规模（输出上限 1MB，乘积控制得小一些）
    res.append(lines(arr(safe_arr(10**5, 2**14))))
    res.append(lines(arr(safe_arr(10**5, 2**31 - 1, zeros=1))))
    res.append(lines(arr(safe_arr(10**5, 2**31 - 1, zeros=3))))
    return res
