from genlib import *
import json


def ref(v):
    return int(str(v), 16)


def expected(text):
    return arr([ref(v) for v in json.loads(text.split("\n")[0])])


def samples():
    res = [
        (lines(arr([59, 23, 12])), "[89,35,18]"),
        (lines(arr([0, 9, 10, 99])), "[0,9,16,153]"),
        (lines(arr([25])), "[37]"),
    ]
    for inp, out in res:
        assert expected(inp) == out
    return res


def cases():
    data = [
        [0],
        [99],
        [9, 10],
        list(range(100)),
        list(range(99, -1, -1)),
        [59, 59, 23, 31, 12, 1],
        [80, 90, 8, 19, 91],
    ]
    for n in (10, 100, 1000):
        data.append(rand_arr(n, 0, 99))
    for _ in range(3):
        data.append(rand_arr(20, 50, 99))
    for vals in data:
        assert 1 <= len(vals) <= 1000
        for v in vals:
            assert 0 <= v <= 99
            assert (ref(v) >> 4) * 10 + (ref(v) & 15) == v
    return [lines(arr(vals)) for vals in data]
