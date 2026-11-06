from genlib import *


def dutch(a):
    a = a[:]
    p0, i, p2 = 0, 0, len(a) - 1
    while i <= p2:
        if a[i] == 0:
            a[i], a[p0] = a[p0], a[i]
            p0 += 1
            i += 1
        elif a[i] == 2:
            a[i], a[p2] = a[p2], a[i]
            p2 -= 1
        else:
            i += 1
    return a


def samples():
    return [
        (lines(arr([2, 0, 2, 1, 1, 0])), "[0,0,1,1,2,2]"),
        (lines(arr([2, 0, 1])), "[0,1,2]"),
    ]


def cases():
    for _ in range(500):
        a = rand_arr(random.randint(1, 12), 0, 2)
        assert dutch(a) == sorted(a)
    return [
        lines(arr([0])),
        lines(arr([1])),
        lines(arr([2])),
        lines(arr([2, 0])),
        lines(arr([1, 0])),
        lines(arr([2, 2, 1, 1, 0, 0])),
        lines(arr([0, 0, 1, 1, 2, 2])),
        lines(arr([2, 1, 2, 1])),
        lines(arr(rand_arr(20, 0, 2))),
        lines(arr([2] * 300)),
        lines(arr([2] * 150 + [0] * 150)),
        lines(arr(rand_arr(300, 0, 2))),
        lines(arr(rand_arr(300, 1, 2))),
        lines(arr(rand_arr(299, 0, 1))),
    ]
