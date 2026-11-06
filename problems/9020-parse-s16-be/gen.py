from genlib import *
import json


def ref(buf):
    res = []
    for i in range(len(buf) // 2):
        u = (buf[2 * i] << 8) | buf[2 * i + 1]
        res.append(u - 65536 if u >= 32768 else u)
    return res


def expected(text):
    return arr(ref(json.loads(text.split("\n")[0])))


def samples():
    res = [
        (lines(arr([18, 52, 255, 254, 128, 0])), "[4660,-2,-32768]"),
        (lines(arr([64, 0, 192, 0, 0, 16])), "[16384,-16384,16]"),
        (lines(arr([127, 255])), "[32767]"),
    ]
    for inp, out in res:
        assert expected(inp) == out
    return res


def cases():
    data = [
        [0, 0],
        [255, 255],
        [128, 1],
        [0, 128, 0, 255, 1, 0],
        [255, 0, 0, 255, 254, 255],
    ]
    for n in (14, 100, 1000):
        data.append(rand_arr(n, 0, 255))
    for _ in range(3):
        data.append(rand_arr(20, 128, 255))
    data.append(rand_arr(1000, 0, 255))
    for buf in data:
        assert len(buf) % 2 == 0 and 2 <= len(buf) <= 1000
        assert ref(buf) == [int.from_bytes(bytes(buf[i:i + 2]), "big", signed=True)
                            for i in range(0, len(buf), 2)]
    return [lines(arr(buf)) for buf in data]
