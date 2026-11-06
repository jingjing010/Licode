from genlib import *
import json


def ref(buf):
    return bytes(buf).hex().upper()


def expected(text):
    return s(ref(json.loads(text.split("\n")[0])))


def samples():
    res = [
        (lines(arr([18, 52, 171, 205])), '"1234ABCD"'),
        (lines(arr([0, 255, 10])), '"00FF0A"'),
        (lines(arr([])), '""'),
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
        [9, 10, 160, 144],
        list(range(16)),
        [0x5A, 0xA5, 0xDE, 0xAD, 0xBE, 0xEF],
        rand_arr(50, 0, 255),
        rand_arr(1000, 0, 255),
        rand_arr(300, 0, 15),
        rand_arr(1000, 160, 255),
        list(range(256)),
    ]
    for buf in data:
        assert len(buf) <= 1000
        assert bytes.fromhex(ref(buf)) == bytes(buf)
        assert len(ref(buf)) == 2 * len(buf)
    return [lines(arr(buf)) for buf in data]
