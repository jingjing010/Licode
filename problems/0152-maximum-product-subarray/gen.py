from genlib import *

LIMIT = 2**31 - 1


def brute(a):
    best = a[0]
    for i in range(len(a)):
        p = 1
        for j in range(i, len(a)):
            p *= a[j]
            best = max(best, p)
    return best


def fast(a):
    mx = mn = ans = a[0]
    for x in a[1:]:
        mx, mn = max(x, mx * x, mn * x), min(x, mx * x, mn * x)
        ans = max(ans, mx)
    return ans


def safe(a):
    """检查：任意子数组乘积的绝对值都不超过 2^31-1（每段非零元素的绝对值之积不超过即可）"""
    p = 1
    for x in a:
        if x == 0:
            p = 1
            continue
        p *= abs(x)
        if p > LIMIT:
            return False
    return True


def gen(n, big_prob, zero_prob, lo=-10, hi=10):
    """大部分是 ±1，偶尔放 |x|>=2 的数（不超出乘积预算），偶尔放 0"""
    a, p = [], 1
    for _ in range(n):
        r = random.random()
        if r < zero_prob:
            a.append(0)
            p = 1
            continue
        if r < zero_prob + big_prob:
            x = random.choice([v for v in range(lo, hi + 1) if abs(v) >= 2])
            if p * abs(x) <= LIMIT:
                a.append(x)
                p *= abs(x)
                continue
        a.append(random.choice([1, -1]))
    assert safe(a)
    return a


def samples():
    return [
        (lines(arr([2, 3, -2, 4])), "6"),
        (lines(arr([-2, 0, -1])), "0"),
    ]


def cases():
    for _ in range(300):
        a = rand_arr(random.randint(1, 10), -10, 10)
        assert brute(a) == fast(a)
    n = 2 * 10**4
    res = [
        [-2],
        [0],
        [10],
        [-2, 3, -4],
        [-1, -1],
        [0, 2],
        [-2, 0, -1, 0, -3],
        [3, -1, 4],
        gen(10, 0.6, 0.1),
        gen(100, 0.3, 0.05),
        gen(1000, 0.05, 0.01),
        [-1] * n,
        [2] * 30 + [0] + [-2] * 30 + [1] * (n - 61),
        gen(n, 0.01, 0.0),
        gen(n, 0.02, 0.002),
        gen(n, 0.3, 0.05),
    ]
    for a in res:
        assert 1 <= len(a) <= n and safe(a) and all(-10 <= x <= 10 for x in a)
    return [lines(arr(a)) for a in res]
