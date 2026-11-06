from genlib import *
import json

INT_MAX = 2**31 - 1
INT_MIN = -2**31


def ref(t):
    i = 0
    while i < len(t) and t[i] == " ":
        i += 1
    sign = 1
    if i < len(t) and t[i] in "+-":
        sign = -1 if t[i] == "-" else 1
        i += 1
    j = i
    while j < len(t) and t[j].isdigit():
        j += 1
    v = sign * int(t[i:j]) if j > i else 0
    return max(INT_MIN, min(INT_MAX, v))


def expected(text):
    return str(ref(json.loads(text.split("\n")[0])))


def samples():
    res = [
        (lines(s("42")), "42"),
        (lines(s("   -1500rpm")), "-1500"),
        (lines(s("99999999999")), "2147483647"),
    ]
    for inp, out in res:
        assert expected(inp) == out
    return res


def cases():
    data = [
        "",
        "-",
        "abc123",
        "+-12",
        "0",
        "  +0012x",
        "2147483647",
        "2147483648",
        "-2147483648",
        "-2147483649",
        "0000000000000000000000000000002147483647",
        "-000000000000000000000000000000000000042",
        "12 34",
        "115200,8,N,1",
        "-" + "9" * 150,
        " " * 100 + "-" + "1" * 9,
        str(random.randint(INT_MIN, INT_MAX)) + rand_str(10),
    ]
    for t in data:
        assert len(t) <= 200 and '"' not in t and "\\" not in t
        r = ref(t)
        assert INT_MIN <= r <= INT_MAX
    return [lines(s(t)) for t in data]
