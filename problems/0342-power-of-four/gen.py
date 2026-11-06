from genlib import *

MIN, MAX = -2**31, 2**31 - 1
POW4 = {4**k for k in range(16)}


def brute(n):
    if n <= 0:
        return False
    while n % 4 == 0:
        n //= 4
    return n == 1


def samples():
    return [
        (lines(16), "true"),
        (lines(5), "false"),
        (lines(1), "true"),
    ]


def cases():
    vals = [0, -1, -4, -16, MIN, MAX, 2, 4, 8, 64, 2**30, 2**29, 2**30 - 1, 2**30 + 1, 3, 4**7]
    vals.append(random.randint(1, MAX))
    for v in range(-100, 5000):
        assert brute(v) == (v in POW4)
    for v in vals:
        assert brute(v) == (v in POW4)
    return [lines(v) for v in vals]
