import json

from genlib import *

PRINTABLE = "".join(chr(c) for c in range(32, 127))


def ref(a, c):
    return len(set(a)) == len(set(c)) == len(set(zip(a, c)))


def _brute(a, c):
    f, g = {}, {}
    for x, y in zip(a, c):
        if f.setdefault(x, y) != y or g.setdefault(y, x) != x:
            return False
    return True


def expected(inp):
    a, c = [json.loads(x) for x in inp.strip().split("\n")]
    return b(ref(a, c))


def iso_pair(n, alpha=PRINTABLE, k=None):
    """随机串 + 随机一一映射得到的同构串"""
    src = alpha if k is None else "".join(random.sample(alpha, k))
    a = rand_str(n, src)
    dst = random.sample(PRINTABLE, len(set(a)))
    m = dict(zip(sorted(set(a)), dst))
    return a, "".join(m[x] for x in a)


def break_one(a, c):
    """修改 c 中的一个字符，使其不再同构"""
    c = list(c)
    while True:
        i = random.randrange(len(c))
        old = c[i]
        c[i] = random.choice(sorted(set(c) - {old}) or PRINTABLE)
        if not ref(a, "".join(c)):
            return "".join(c)
        c[i] = old


def case(a, c):
    assert len(a) == len(c) >= 1
    return lines(s(a), s(c))


for _ in range(500):
    _n = random.randint(1, 8)
    _a, _c = rand_str(_n, "abc"), rand_str(_n, "xyz")
    assert ref(_a, _c) == _brute(_a, _c)


def samples():
    return [
        (case("egg", "add"), "true"),
        (case("foo", "bar"), "false"),
        (case("paper", "title"), "true"),
    ]


def cases():
    res = [
        case("a", "a"),
        case("a", "b"),
        case("ab", "aa"),
        case("aa", "ab"),
        case("badc", "baba"),
        case('a"\\ ', '\\ "a'),
    ]
    a, c = iso_pair(10, "abcd")
    res.append(case(a, c))
    a, c = iso_pair(100, "abcdefghij")
    res.append(case(a, break_one(a, c)))
    a, c = iso_pair(5 * 10**4)
    res.append(case(a, c))
    a, c = iso_pair(5 * 10**4)
    res.append(case(a, break_one(a, c)))
    a, c = iso_pair(5 * 10**4, "ab")
    res.append(case(a, c))
    res.append(case("a" * (5 * 10**4), "b" * (5 * 10**4 - 1) + "c"))
    res.append(case(PRINTABLE * 500, PRINTABLE[::-1] * 500))
    return res
