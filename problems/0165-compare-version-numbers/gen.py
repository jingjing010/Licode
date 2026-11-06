import json

from genlib import *

INT_MAX = 2**31 - 1


def ref(v1, v2):
    a = [int(x) for x in v1.split(".")]
    b = [int(x) for x in v2.split(".")]
    n = max(len(a), len(b))
    a += [0] * (n - len(a))
    b += [0] * (n - len(b))
    return (a > b) - (a < b)


def expected(inp):
    v1, v2 = [json.loads(x) for x in inp.strip().split("\n")]
    return str(ref(v1, v2))


def rev(val, zeros=0):
    return "0" * zeros + str(val)


def version(k, hi=20, zmax=2):
    return ".".join(rev(random.randint(0, hi), random.randint(0, zmax)) for _ in range(k))


def perturb(v):
    """同一个版本号的另一种写法：随机加前导零、在末尾补 .0"""
    parts = [rev(int(x), random.randint(0, 2)) for x in v.split(".")]
    parts += ["0" * random.randint(1, 2)] * random.randint(0, 3)
    return ".".join(parts)


def case(a, b):
    assert 1 <= len(a) <= 500 and 1 <= len(b) <= 500
    for x in a.split(".") + b.split("."):
        assert x.isdigit() and int(x) <= INT_MAX
    return lines(s(a), s(b))


def samples():
    return [
        (case("1.2", "1.10"), "-1"),
        (case("1.01", "1.001"), "0"),
        (case("1.0", "1.0.0.0"), "0"),
    ]


def cases():
    res = [
        case("0", "0"),
        case("1", "0"),
        case("1.0.1", "1"),
        case("7.5.2.4", "7.5.3"),
        case("2147483647", "2147483646"),
        case("0" * 490 + "2147483647", "2147483647"),
        case("1." + "0" * 497 + "1", "1.1"),
        case(".".join(["0"] * 250), "0"),
        case(".".join(["0"] * 249) + ".1", ".".join(["0"] * 250)),
    ]
    v = version(8)
    res.append(case(v, perturb(v)))
    for _ in range(3):
        res.append(case(version(random.randint(1, 6), 3, 1), version(random.randint(1, 6), 3, 1)))
    big = ".".join(rev(random.randint(0, INT_MAX)) for _ in range(40))
    res.append(case(big, big + ".0"))
    big2 = big.rsplit(".", 1)[0] + "." + str(int(big.rsplit(".", 1)[1]) ^ 1)
    res.append(case(big, big2))
    return res


for _ in range(300):
    _a = version(random.randint(1, 5), 3, 1)
    assert ref(_a, perturb(_a)) == 0
