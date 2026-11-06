from genlib import *


def ref(n):
    return [bin(i).count("1") for i in range(n + 1)]


def ref_dp(n):
    a = [0] * (n + 1)
    for i in range(1, n + 1):
        a[i] = a[i & (i - 1)] + 1
    return a


def samples():
    return [
        (lines(2), "[0,1,1]"),
        (lines(5), "[0,1,1,2,1,2]"),
    ]


def cases():
    ns = [0, 1, 3, 8, 16, 31, 100, 1023, 1024, 65535, 65536, 99999, 10**5]
    ns.append(random.randint(1000, 10**5))
    assert ref(10**5) == ref_dp(10**5)
    assert ref(2) == [0, 1, 1] and ref(5) == [0, 1, 1, 2, 1, 2]
    return [lines(n) for n in ns]
