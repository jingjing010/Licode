from genlib import *


def ref(x):
    return int.from_bytes(x.to_bytes(4, "big"), "little")


def expected(text):
    return str(ref(int(text.split()[0])))


def samples():
    res = [
        (lines(305419896), "2018915346"),
        (lines(4278190080), "255"),
        (lines(1), "16777216"),
    ]
    for inp, out in res:
        assert expected(inp) == out
    return res


def cases():
    vals = [0, 0xFFFFFFFF, 0x80000000, 0x7FFFFFFF, 0x000000FF,
            0x0000FF00, 0x00FF0000, 0xC0A80001, 0xDEADBEEF, 0x01020304]
    for _ in range(6):
        vals.append(random.randint(0, 0xFFFFFFFF))
    for v in vals:
        assert ref(ref(v)) == v
    return [lines(v) for v in vals]
