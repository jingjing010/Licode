from genlib import *

LIM = 3 * 10**4


def make(pairs, lo=-LIM, hi=LIM, single=None):
    """pairs 个成对出现的不同数 + 1 个只出现一次的数，随机打乱"""
    vals = rand_distinct(pairs + 1, lo, hi)
    if single is not None:
        vals = [v for v in vals if v != single][:pairs] + [single]
    a = vals[:pairs] * 2 + [vals[pairs]]
    random.shuffle(a)
    return a


def samples():
    return [
        (lines(arr([2, 2, 1])), "1"),
        (lines(arr([4, 1, 2, 1, 2])), "4"),
        (lines(arr([1])), "1"),
    ]


def cases():
    for _ in range(200):
        a = make(random.randint(0, 10), -20, 20)
        c = {x: a.count(x) for x in a}
        assert sorted(c.values()).count(1) == 1
    big = (LIM - 1) // 2
    return [
        lines(arr([-30000])),
        lines(arr([0, 7, 7])),
        lines(arr([-1, -1, -2])),
        lines(arr([30000, -30000, 30000])),
        lines(arr(make(5))),
        lines(arr(make(100, -50, 50))),
        lines(arr(make(1000))),
        lines(arr(make(big))),
        lines(arr(make(big, single=0))),
        lines(arr(make(big, single=-30000))),
        lines(arr(sorted(make(big)))),
        lines(arr(make(big, 0, LIM))),
    ]
