from genlib import *
import json
import re


def ref(t):
    i = 0
    while i < len(t) and t[i] == " ":
        i += 1
    sign = 1
    if i < len(t) and t[i] in "+-":
        sign = -1 if t[i] == "-" else 1
        i += 1
    j = i
    while j < len(t) and "0" <= t[j] <= "9":
        j += 1
    v = sign * int(t[i:j]) if j > i else 0
    return max(-2 ** 31, min(2 ** 31 - 1, v))


def ref2(t):
    m = re.match(r" *([+-]?[0-9]+)", t)
    v = int(m.group(1)) if m else 0
    return max(-2 ** 31, min(2 ** 31 - 1, v))


def expected(text):
    return str(ref(json.loads(text.split("\n")[0])))


def samples():
    res = [
        (lines(s("1500")), "1500"),
        (lines(s("  -42mV")), "-42"),
        (lines(s("AT+CSQ")), "0"),
    ]
    for inp, out in res:
        assert expected(inp) == out
    return res


def cases():
    data = [
        "",
        "   ",
        "0",
        "-0",
        "+7",
        "+-2",
        "-",
        "--5",
        " + 5",
        "2147483647",
        "2147483648",
        "-2147483648",
        "-2147483649",
        "99999999999999999999999",
        "-000000000000000000000000000123",
        " 12 34",
        "3.14",
        "\t5",
        "-1500\r\n",
        "4294967296",
        "x123",
        " " * 150 + "-" + "9" * 40,
        "%d" % random.randint(-2 ** 31, 2 ** 31 - 1) + "abc",
    ]
    for t in data:
        assert len(t) <= 200
        assert ref(t) == ref2(t)
    return [lines(s(t)) for t in data]
