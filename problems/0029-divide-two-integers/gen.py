from genlib import *

MIN, MAX = -2**31, 2**31 - 1


def ref(a, b):
    q = abs(a) // abs(b)
    if (a < 0) != (b < 0):
        q = -q
    return max(MIN, min(MAX, q))


def ref_bits(a, b):
    """模拟 solution.c 的逐位长除法"""
    if a == MIN and b == -1:
        return MAX
    ua, ub, q = abs(a), abs(b), 0
    for i in range(31, -1, -1):
        if (ua >> i) >= ub:
            ua -= ub << i
            q |= 1 << i
    return -q if (a < 0) != (b < 0) else q


def samples():
    return [
        (lines(10, 3), "3"),
        (lines(7, -3), "-2"),
    ]


def cases():
    fixed = [
        (MIN, -1), (MIN, 1), (MIN, MIN), (MAX, MIN), (MAX, 1), (MAX, -1),
        (MIN, 2), (MIN, -3), (0, 5), (1, 1), (-1, 1), (1, 2), (-7, 3), (MAX, MAX),
    ]
    rnd = []
    for _ in range(3):
        a = random.randint(MIN, MAX)
        b = random.randint(1, 1000) * random.choice([1, -1])
        rnd.append((a, b))
    rnd.append((random.randint(MIN, MAX), random.randint(MIN, MAX) or 1))
    for _ in range(5000):
        a = random.randint(MIN, MAX)
        b = random.choice([random.randint(-50, 50), random.randint(MIN, MAX)]) or 1
        assert ref(a, b) == ref_bits(a, b)
    for a, b in fixed:
        assert ref(a, b) == ref_bits(a, b)
    assert ref(10, 3) == 3 and ref(7, -3) == -2 and ref(MIN, -1) == MAX
    return [lines(a, b) for a, b in fixed + rnd]
