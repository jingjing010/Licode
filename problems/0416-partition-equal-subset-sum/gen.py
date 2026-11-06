from genlib import *


def brute(a):
    total = sum(a)
    if total % 2:
        return False
    n = len(a)
    return any(2 * sum(a[i] for i in range(n) if mask >> i & 1) == total for mask in range(1 << n))


def fast(a):
    total = sum(a)
    if total % 2:
        return False
    reach = 1
    for x in a:
        reach |= reach << x
    return bool(reach >> (total // 2) & 1)


def samples():
    return [
        (lines(arr([1, 5, 11, 5])), "true"),
        (lines(arr([1, 2, 3, 5])), "false"),
    ]


def cases():
    for _ in range(300):
        a = rand_arr(random.randint(1, 12), 1, 20)
        assert brute(a) == fast(a)
    big_even = [random.choice(range(2, 101, 2)) for _ in range(200)]
    big_even[0] = 100
    # 偶数和但凑不出：除一个大数外全部是偶数且很小
    tricky = [2] * 10 + [100]
    res = [
        [1],
        [100],
        [1, 1],
        [1, 2],
        [2, 2, 3, 5],
        [3, 3, 3, 4, 5],
        tricky,
        rand_arr(10, 1, 20),
        rand_arr(50, 1, 100),
        [100] * 200,
        [100] * 199 + [1],
        [1] * 199 + [99],
        [99] * 2 + [2] * 198,
        rand_arr(200, 1, 100),
        rand_arr(200, 90, 100),
        big_even[:199] + [1],
    ]
    return [lines(arr(a)) for a in res]
