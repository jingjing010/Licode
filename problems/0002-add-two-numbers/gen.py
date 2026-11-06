from genlib import *


def num(n):
    """n 位随机数的逆序数字列表（最高位非 0）"""
    if n == 1:
        return [random.randint(0, 9)]
    return rand_arr(n - 1, 0, 9) + [random.randint(1, 9)]


def to_int(d):
    return int("".join(map(str, reversed(d))))


def brute(inp):
    ls = inp.split("\n")
    a = [int(x) for x in ls[0].strip("[]").split(",")]
    c = [int(x) for x in ls[1].strip("[]").split(",")]
    return arr([int(ch) for ch in reversed(str(to_int(a) + to_int(c)))])


def samples():
    res = [
        (lines(arr([2, 4, 3]), arr([5, 6, 4])), "[7,0,8]"),
        (lines(arr([0]), arr([0])), "[0]"),
        (lines(arr([9] * 7), arr([9] * 4)), "[8,9,9,9,0,0,0,1]"),
    ]
    for inp, want in res:
        assert brute(inp) == want
    return res


def cases():
    res = [
        lines(arr([5]), arr([5])),
        lines(arr([0]), arr([7, 3])),
        lines(arr([1]), arr([9] * 100)),
        lines(arr([9] * 100), arr([9] * 100)),
        lines(arr([1] + [0] * 98 + [1]), arr([9] * 99)),
        lines(arr(num(3)), arr(num(10))),
        lines(arr(num(50)), arr(num(50))),
        lines(arr(num(100)), arr(num(1))),
        lines(arr(num(100)), arr(num(100))),
        lines(arr(num(37)), arr(num(99))),
        lines(arr([5] * 100), arr([5] * 100)),
        lines(arr([0] * 99 + [1]), arr([0] * 99 + [9])),
        lines(arr([random.choice([4, 5]) for _ in range(99)] + [5]), arr([5] * 100)),
    ]
    return res
