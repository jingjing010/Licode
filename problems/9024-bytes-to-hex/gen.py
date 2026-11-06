from genlib import *
import json


def ref(buf):
    return bytes(buf).hex().upper()


def expected(text):
    return s(ref(json.loads(text.split("\n")[0])))


def samples():
    res = [
        (lines(arr([18, 52, 171, 205])), s("1234ABCD")),
        (lines(arr([0, 255, 10])), s("00FF0A")),
        (lines(arr([])), s("")),
    ]
    for inp, out in res:
        assert expected(inp) == out
    return res


def cases():
    data = [
        [0],
        [255],
        [15],
        [16],
        [160, 11, 1, 240],
        list(range(16)),
        [i * 16 for i in range(16)],
        [0, 0, 0, 0, 0],
    ]
    for n in (20, 300, 1000):
        data.append(rand_arr(n, 0, 255))
    data.append(rand_arr(1000, 0, 15))
    data.append(list(range(256)))
    for buf in data:
        assert len(buf) <= 1000
        assert list(bytes.fromhex(ref(buf))) == buf
    return [lines(arr(buf)) for buf in data]
