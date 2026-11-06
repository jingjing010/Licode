import json
import sys

from genlib import *

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(100000)


def ref(a, c):
    return str(int(a) + int(c))


def expected(inp):
    a, c = [json.loads(x) for x in inp.strip().split("\n")]
    return s(ref(a, c))


def num(n):
    if n == 1:
        return str(random.randint(0, 9))
    return str(random.randint(1, 9)) + rand_str(n - 1, "0123456789")


def case(a, c):
    return lines(s(a), s(c))


def samples():
    return [
        (case("11", "123"), '"134"'),
        (case("456", "77"), '"533"'),
        (case("0", "0"), '"0"'),
    ]


def cases():
    N = 10**4
    return [
        case("0", "9"),
        case("9", "1"),
        case("1", "9" * 30),
        case("9" * 30, "1"),
        case("5", "5"),
        case(num(18), num(19)),
        case(num(20), num(500)),
        case("9" * N, "9" * N),
        case("9" * N, "1"),
        case("1" + "0" * (N - 1), "0"),
        case(num(N), num(N)),
        case(num(N), num(1)),
        case(num(N - 1), num(N)),
    ]
