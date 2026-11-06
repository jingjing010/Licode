from genlib import *

MAX = 2**31 - 1


def brute(l, r):
    v = l
    for x in range(l + 1, r + 1):
        v &= x
        if v == 0:
            break
    return v


def ref(l, r):
    shift = 0
    while l != r:
        l >>= 1
        r >>= 1
        shift += 1
    return l << shift


def samples():
    return [
        (lines(5, 7), "4"),
        (lines(0, 0), "0"),
        (lines(1, MAX), "0"),
    ]


def cases():
    pairs = [
        (MAX, MAX), (0, MAX), (2**30, MAX), (2**30 - 1, 2**30), (6, 7), (12, 15),
        (2**31 - 2, MAX), (1, 1), (0, 1),
    ]
    for _ in range(3):
        l = random.randint(0, MAX)
        pairs.append((l, min(MAX, l + random.randint(0, 1000))))
    for _ in range(3):
        a, b = random.randint(0, MAX), random.randint(0, MAX)
        pairs.append((min(a, b), max(a, b)))
    pairs.append((0b1011 << 20, (0b1011 << 20) | 0xFFFFF))
    for _ in range(3000):
        l = random.randint(0, 5000)
        r = l + random.randint(0, 300)
        assert brute(l, r) == ref(l, r)
    for l, r in pairs:
        if r - l <= 10**5:
            assert brute(l, r) == ref(l, r)
    assert ref(5, 7) == 4 and ref(0, 0) == 0 and ref(1, MAX) == 0
    return [lines(l, r) for l, r in pairs]
