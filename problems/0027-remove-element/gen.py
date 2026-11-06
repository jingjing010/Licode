from genlib import *


def brute(a, val):
    kept = sorted(x for x in a if x != val)
    return "%d\n%s" % (len(kept), arr(kept))


def samples():
    res = []
    for a, val, want in (([3, 2, 2, 3], 3, "2\n[2,2]"),
                         ([0, 1, 2, 2, 3, 0, 4, 2], 2, "5\n[0,0,1,3,4]")):
        assert brute(a, val) == want
        res.append((lines(arr(a), val), want))
    return res


def cases():
    res = [
        lines(arr([]), 0),
        lines(arr([1]), 1),
        lines(arr([1]), 2),
        lines(arr([4, 4, 4, 4]), 4),
        lines(arr([1, 2, 3, 4, 5]), 100),
        lines(arr([0, 0, 1]), 0),
        lines(arr([2, 3, 3, 3]), 3),
        lines(arr([50] * 100), 50),
        lines(arr(list(range(51)) + list(range(49))), 50),
    ]
    for n, hi in ((10, 3), (30, 5), (60, 10)):
        a = rand_arr(n, 0, hi)
        res.append(lines(arr(a), random.choice(a)))
    for _ in range(3):
        a = rand_arr(100, 0, 50)
        res.append(lines(arr(a), random.choice(a)))
    res.append(lines(arr(rand_arr(100, 0, 50)), 77))
    return res
