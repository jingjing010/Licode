import json

from genlib import *


def brute(inp):
    a = json.loads(inp.split("\n")[0])
    return b(a == a[::-1])


def palin(n, lo=0, hi=9):
    half = rand_arr(n // 2, lo, hi)
    mid = rand_arr(n % 2, lo, hi)
    return half + mid + half[::-1]


def near_palin(n):
    a = palin(n)
    i = random.randrange(n // 2)
    a[i] = (a[i] + random.randint(1, 9)) % 10
    return a


def samples():
    res = [
        (lines(arr([1, 2, 2, 1])), "true"),
        (lines(arr([1, 2])), "false"),
    ]
    for inp, want in res:
        assert brute(inp) == want
    return res


def cases():
    res = [
        lines(arr([5])),
        lines(arr([1, 1])),
        lines(arr([1, 0, 1])),
        lines(arr([1, 0, 0])),
        lines(arr([1, 2, 3, 2, 1])),
        lines(arr([1, 2, 3, 1, 2])),
    ]
    for n in (7, 20, 101):
        res.append(lines(arr(palin(n))))
        res.append(lines(arr(near_palin(n))))
    res.append(lines(arr(rand_arr(1000, 0, 9))))
    res.append(lines(arr(palin(10**5))))
    res.append(lines(arr(palin(10**5 - 1))))
    res.append(lines(arr(near_palin(10**5))))
    res.append(lines(arr([7] * 10**5)))
    return res
