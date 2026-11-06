from genlib import *


def samples():
    return [
        (lines(arr([1, 0, 0])), "true"),
        (lines(arr([1, 1, 1, 0])), "false"),
    ]


def decode_last_is_one(bits):
    i = 0
    last = None
    while i < len(bits):
        last = 1 if bits[i] == 0 else 2
        i += last
    return last == 1


def tail_ones(bits):
    k = 0
    for x in reversed(bits[:-1]):
        if x != 1:
            break
        k += 1
    return k % 2 == 0


def rand_bits(n, p=0.5):
    return [1 if random.random() < p else 0 for _ in range(n - 1)] + [0]


for _ in range(500):
    _b = rand_bits(random.randint(1, 12), 0.6)
    assert decode_last_is_one(_b) == tail_ones(_b)


def cases():
    res = [
        lines(arr([0])),
        lines(arr([1, 0])),
        lines(arr([0, 0])),
        lines(arr([1, 1, 0])),
        lines(arr([0, 1, 0])),
        lines(arr([1] * 999 + [0])),
        lines(arr([1] * 998 + [0])),
        lines(arr([0] * 1000)),
    ]
    for n in (10, 50, 1000):
        res.append(lines(arr(rand_bits(n))))
    res.append(lines(arr(rand_bits(1000, 0.9))))
    res.append(lines(arr(rand_bits(1000, 0.9))))
    return res
