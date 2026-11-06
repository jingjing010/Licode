from genlib import *
import json


def ref(buf, offset):
    return int.from_bytes(bytes(buf[offset:offset + 4]), "big")


def expected(text):
    ls = text.split("\n")
    return str(ref(json.loads(ls[0]), int(ls[1])))


def samples():
    res = [
        (lines(arr([18, 52, 86, 120]), 0), "305419896"),
        (lines(arr([170, 0, 1, 134, 160, 85]), 1), "100000"),
        (lines(arr([1, 255, 255, 255, 255]), 1), "4294967295"),
    ]
    for inp, out in res:
        assert expected(inp) == out
    return res


def cases():
    data = [
        ([0, 0, 0, 0], 0),
        ([128, 0, 0, 0], 0),
        ([0, 0, 0, 128], 0),
        ([127, 255, 255, 255], 0),
        ([255, 1, 2, 3, 4], 0),
        ([9, 8, 7, 6, 5, 4, 3, 2, 1], 5),
    ]
    for n in (7, 50, 1000):
        data.append((rand_arr(n, 0, 255), random.randint(0, n - 4)))
    for _ in range(3):
        data.append((rand_arr(20, 128, 255), random.randint(0, 16)))
    data.append((rand_arr(1000, 0, 255), 996))
    for buf, off in data:
        assert 0 <= off and off + 4 <= len(buf) <= 1000
        assert 0 <= ref(buf, off) <= 0xFFFFFFFF
    return [lines(arr(buf), off) for buf, off in data]
