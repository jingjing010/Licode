import json

from genlib import *


def ref(a, b):
    return bin(int(a, 2) + int(b, 2))[2:]


def expected(inp):
    a, b = [json.loads(x) for x in inp.strip().split("\n")]
    return s(ref(a, b))


def bnum(n):
    if n == 1:
        return random.choice("01")
    return "1" + rand_str(n - 1, "01")


def case(a, b):
    return lines(s(a), s(b))


def samples():
    return [
        (case("11", "1"), '"100"'),
        (case("1010", "1011"), '"10101"'),
    ]


def cases():
    n = 10**4
    return [
        case("0", "0"),
        case("0", "1"),
        case("1", "0"),
        case("1", "1"),
        case("1" * 10, "1"),
        case("1", "1" * 50),
        case(bnum(7), bnum(3)),
        case(bnum(64), bnum(64)),
        case(bnum(1000), bnum(10)),
        case("1" * n, "1" * n),
        case("1" * n, "1"),
        case("1" + "0" * (n - 1), "0"),
        case(bnum(n), bnum(n)),
        case(bnum(n), bnum(5000)),
    ]
