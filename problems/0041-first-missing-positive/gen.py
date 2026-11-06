from genlib import *

INT_MIN, INT_MAX = -2**31, 2**31 - 1


def samples():
    return [
        (lines(arr([1, 2, 0])), "3"),
        (lines(arr([3, 4, -1, 1])), "2"),
        (lines(arr([7, 8, 9, 11, 12])), "1"),
    ]


def brute(nums):
    st = set(nums)
    x = 1
    while x in st:
        x += 1
    return x


def fast(nums):
    a, n = list(nums), len(nums)
    for i in range(n):
        while 1 <= a[i] <= n and a[a[i] - 1] != a[i]:
            j = a[i] - 1
            a[i], a[j] = a[j], a[i]
    for i in range(n):
        if a[i] != i + 1:
            return i + 1
    return n + 1


for _ in range(500):
    _a = rand_arr(random.randint(1, 12), -3, 14)
    assert brute(_a) == fast(_a)


def missing_one(n, miss):
    """1..n+1 去掉 miss 后打乱，答案就是 miss"""
    a = [x for x in range(1, n + 2) if x != miss]
    random.shuffle(a)
    return a


def cases():
    N = 10**5
    res = [
        lines(arr([1])),
        lines(arr([2])),
        lines(arr([-1])),
        lines(arr([1, 1])),
        lines(arr([2, 2, 2, 1])),
        lines(arr([INT_MIN, INT_MAX, 0, 1])),
        lines(arr([2, 1])),
        lines(arr([5, 4, 3, 2, 1])),
    ]
    res.append(lines(arr(rand_arr(30, -10, 30))))
    res.append(lines(arr(rand_arr(1000, -500, 900))))
    res.append(lines(arr(perm(N))))
    res.append(lines(arr(missing_one(N - 1, random.randint(1, N - 1)))))
    res.append(lines(arr(missing_one(N - 1, 1))))
    res.append(lines(arr(rand_arr(N, INT_MIN, INT_MAX))))
    dup = [random.randint(1, N // 2) for _ in range(N)]
    res.append(lines(arr(dup)))
    res.append(lines(arr([random.choice((INT_MIN, -1, 0, INT_MAX, N + 1)) for _ in range(N)])))
    return res
