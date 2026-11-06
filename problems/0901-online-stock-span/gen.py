from genlib import *

N = 10**4
XCHECK_LIMIT = 30000


def brute(prices):
    out = []
    for i, p in enumerate(prices):
        j = i
        while j >= 0 and prices[j] <= p:
            j -= 1
        out.append(i - j)
    return out


def fmt(spans):
    return "[" + ",".join(["null"] + [str(x) for x in spans]) + "]"


def case(prices):
    ops = ["StockSpanner"] + ["next"] * len(prices)
    return lines(sarr(ops), "[" + ",".join(["[]"] + ["[%d]" % p for p in prices]) + "]")


def expect(inp):
    import json
    args = json.loads(inp.splitlines()[1])
    return fmt(brute([a[0] for a in args[1:]]))


def samples():
    prices = [100, 80, 60, 70, 60, 75, 85]
    want = "[null,1,1,1,2,1,4,6]"
    assert fmt(brute(prices)) == want
    return [(case(prices), want)]


def cases():
    res = [
        case([1]),
        case([5, 5, 5, 5]),
        case([1, 2, 3, 4, 5]),
        case([5, 4, 3, 2, 1]),
        case([31, 41, 48, 59, 79]),
    ]
    for n, hi in ((20, 10), (200, 100), (2000, 10**5)):
        res.append(case(rand_arr(n, 1, hi)))
    res.append(case(list(range(1, N + 1))))
    res.append(case(list(range(10**5, 10**5 - N, -1))))
    res.append(case([7] * N))
    res.append(case(rand_arr(N, 1, 10**5)))
    res.append(case(rand_arr(N, 1, 5)))
    res.append(case(list(range(N // 2, 0, -1)) + [10**5] * (N // 2)))
    return res
