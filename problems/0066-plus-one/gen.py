from genlib import *


def brute(d):
    v = int("".join(map(str, d))) + 1
    return arr([int(c) for c in str(v)])


def samples():
    res = []
    for d, want in (([1, 2, 3], "[1,2,4]"), ([4, 3, 2, 1], "[4,3,2,2]"), ([9], "[1,0]")):
        assert brute(d) == want
        res.append((lines(arr(d)), want))
    return res


def rand_num(n):
    return [random.randint(1, 9)] + rand_arr(n - 1, 0, 9)


def cases():
    res = [
        lines(arr([0])),
        lines(arr([8])),
        lines(arr([9, 9])),
        lines(arr([1, 9, 9])),
        lines(arr([1, 0, 0])),
        lines(arr([2, 9, 0, 9])),
        lines(arr([9] * 100)),
        lines(arr([8] + [9] * 99)),
        lines(arr([1] + [0] * 99)),
        lines(arr([9] * 99 + [8])),
    ]
    for n in (5, 20, 100, 100):
        res.append(lines(arr(rand_num(n))))
    res.append(lines(arr(rand_num(50)[:-6] + [9] * 6)))
    return res
