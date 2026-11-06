import json

from genlib import *


def ref(inp):
    ls = inp.split("\n")
    a, b = json.loads(ls[0]), json.loads(ls[1])
    x = int("".join(map(str, a))) + int("".join(map(str, b)))
    return arr([int(c) for c in str(x)])


def num(n):
    if n == 1:
        return [random.randint(0, 9)]
    return [random.randint(1, 9)] + rand_arr(n - 1, 0, 9)


def samples():
    res = [
        (lines(arr([7, 2, 4, 3]), arr([5, 6, 4])), "[7,8,0,7]"),
        (lines(arr([2, 4, 3]), arr([5, 6, 4])), "[8,0,7]"),
        (lines(arr([0]), arr([0])), "[0]"),
    ]
    for inp, want in res:
        assert ref(inp) == want
    return res


def cases():
    res = [
        lines(arr([5]), arr([5])),
        lines(arr([9]), arr([1])),
        lines(arr([0]), arr([1, 2, 3])),
        lines(arr([9] * 100), arr([1])),
        lines(arr([9] * 100), arr([9] * 100)),
        lines(arr([1] + [0] * 99), arr([9] * 99)),
        lines(arr([1, 2, 3]), arr([0])),
    ]
    for n1, n2 in ((3, 5), (10, 10), (50, 7), (1, 100)):
        res.append(lines(arr(num(n1)), arr(num(n2))))
    for _ in range(3):
        res.append(lines(arr(num(100)), arr(num(100))))
    return res
