from genlib import *


def samples():
    return [
        (lines(arr([1, 2, 3, 4, 5, 6, 7, 8]), 2, 0, 5), "[1,2,1,2,3,4,5,8]"),
        (lines(arr([1, 2, 3, 4, 5, 6, 7, 8]), 0, 3, 5), "[4,5,6,7,8,6,7,8]"),
        (lines(arr([10, 20, 30]), 1, 1, 2), "[10,20,30]"),
    ]


def case(length, d, s, n):
    return lines(arr(rand_arr(length, 0, 255)), d, s, n)


def cases():
    res = [
        lines(arr([7]), 0, 0, 1),
        lines(arr([7]), 0, 0, 0),
        lines(arr([1, 2]), 1, 0, 1),
        lines(arr([1, 2]), 0, 1, 1),
        lines(arr([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]), 1, 0, 9),
        lines(arr([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]), 0, 1, 9),
        lines(arr([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]), 6, 0, 4),
        lines(arr([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]), 0, 6, 4),
    ]
    for _ in range(3):
        length = random.randint(20, 200)
        n = random.randint(1, length - 1)
        d, s = random.randint(0, length - n), random.randint(0, length - n)
        res.append(case(length, d, s, n))
    N = 10**5
    res.append(case(N, 3, 0, N - 3))
    res.append(case(N, 0, 5, N - 5))
    res.append(case(N, 50000, 0, 50000))
    return res
