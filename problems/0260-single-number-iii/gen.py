from genlib import *
from collections import Counter

MIN, MAX = -2**31, 2**31 - 1


def make(k, lo=MIN, hi=MAX, singles=None):
    """k 个各出现两次的不同数 + 2 个只出现一次的数，打乱顺序"""
    vals = set(singles or [])
    while len(vals) < k + 2:
        vals.add(random.randint(lo, hi))
    vals = list(vals)
    if singles is None:
        singles = vals[-2:]
    pairs = [v for v in vals if v not in singles][:k]
    a = pairs * 2 + list(singles)
    random.shuffle(a)
    return a, sorted(singles)


def brute(a):
    return sorted(x for x, c in Counter(a).items() if c == 1)


def ref_xor(a):
    x = 0
    for v in a:
        x ^= v & 0xFFFFFFFF
    low = x & -x
    p = q = 0
    for v in a:
        if (v & 0xFFFFFFFF) & low:
            p ^= v
        else:
            q ^= v
    return sorted([p, q])


def samples():
    return [
        (lines(arr([1, 2, 1, 3, 2, 5])), "[3,5]"),
        (lines(arr([-1, 0])), "[-1,0]"),
        (lines(arr([0, 1])), "[0,1]"),
    ]


def cases():
    res = []

    def add(a, want):
        assert brute(a) == want == ref_xor(a)
        res.append(lines(arr(a)))

    add([MIN, MAX], [MIN, MAX])
    add([MIN, 0], [MIN, 0])
    add([-1, -2, -1, -3], [-3, -2])
    add([MAX, 7, MAX, MIN, 8, MIN], [7, 8])
    add([4, 1, 2, 1, 2, 6], [4, 6])
    for k, lo, hi in [(10, -20, 20), (100, -1000, 1000), (1000, MIN, MAX)]:
        add(*make(k, lo, hi))
    big = (3 * 10**4 - 2) // 2
    add(*make(big))
    add(*make(big, singles=[MIN, MAX]))
    add(*make(big, singles=[-1, 1]))
    add(*make(big, singles=[0, MIN]))
    a, want = make(big, -10**5, 10**5)
    add(sorted(a), want)
    for _ in range(300):
        a, want = make(random.randint(0, 8), -30, 30)
        assert brute(a) == want == ref_xor(a)
    return res
