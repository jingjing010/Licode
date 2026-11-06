from genlib import *

MAX = 2**31 - 1


def brute(n):
    return int("".join("1" if c == "0" else "0" for c in bin(n)[2:]), 2)


def ref(n):
    return n ^ ((1 << n.bit_length()) - 1)


def samples():
    return [
        (lines(5), "2"),
        (lines(1), "0"),
    ]


def cases():
    vals = [2, 3, 7, 8, 10, 2**30, 2**30 - 1, 2**30 + 1, MAX, MAX - 1, 0x55555555, 0x2AAAAAAA, 1000]
    for _ in range(4):
        vals.append(random.randint(1, MAX))
    for v in list(range(1, 5000)) + [random.randint(1, MAX) for _ in range(3000)]:
        assert brute(v) == ref(v)
    for v in vals:
        assert brute(v) == ref(v)
    return [lines(v) for v in vals]
