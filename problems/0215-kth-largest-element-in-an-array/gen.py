from genlib import *

N = 10**5
V = 10**4


def brute(a, k):
    return sorted(a, reverse=True)[k - 1]


def samples():
    assert brute([3, 2, 1, 5, 6, 4], 2) == 5
    assert brute([3, 2, 3, 1, 2, 4, 5, 5, 6], 4) == 4
    return [
        (lines(arr([3, 2, 1, 5, 6, 4]), 2), "5"),
        (lines(arr([3, 2, 3, 1, 2, 4, 5, 5, 6]), 4), "4"),
    ]


def cases():
    res = [
        lines(arr([1]), 1),
        lines(arr([-V]), 1),
        lines(arr([2, 1]), 1),
        lines(arr([2, 1]), 2),
        lines(arr([5, 5, 5, 5]), 3),
        lines(arr([-1, -1, -2, -3]), 2),
        lines(arr([V, -V, 0]), 3),
    ]
    for n in (10, 100, 1000):
        a = rand_arr(n, -V, V)
        res.append(lines(arr(a), random.randint(1, n)))
    res.append(lines(arr(rand_arr(N, -V, V)), 1))
    res.append(lines(arr(rand_arr(N, -V, V)), N))
    res.append(lines(arr(rand_arr(N, -V, V)), N // 2))
    res.append(lines(arr([7] * N), 12345))
    res.append(lines(arr(sorted(rand_arr(N, -V, V))), 777))
    res.append(lines(arr(sorted(rand_arr(N, -V, V), reverse=True)), N - 3))
    res.append(lines(arr(rand_arr(N, 0, 2)), 50000))
    return res
