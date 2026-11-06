from genlib import *

N, V = 3 * 10**4, 3 * 10**4
MOD = 10**9 + 7
XCHECK_LIMIT = 20000


def brute(a):
    total = 0
    for i in range(len(a)):
        m = a[i]
        for j in range(i, len(a)):
            m = min(m, a[j])
            total += m
    return total % MOD


def expect(inp):
    import json
    return str(brute(json.loads(inp.splitlines()[0])))


def samples():
    res = []
    for a, want in (([3, 1, 2, 4], 17), ([11, 81, 94, 43, 3], 444)):
        assert brute(a) == want
        res.append((lines(arr(a)), str(want)))
    return res


def cases():
    res = [
        lines(arr([1])),
        lines(arr([30000])),
        lines(arr([2, 2, 2, 2])),
        lines(arr([1, 2, 3, 4, 5])),
        lines(arr([5, 4, 3, 2, 1])),
    ]
    for n, hi in ((10, 5), (100, 50), (1000, V)):
        res.append(lines(arr(rand_arr(n, 1, hi))))
    res.append(lines(arr([V] * N)))
    res.append(lines(arr(list(range(1, N + 1)))))
    res.append(lines(arr(list(range(N, 0, -1)))))
    res.append(lines(arr(rand_arr(N, 1, V))))
    res.append(lines(arr(rand_arr(N, 1, 3))))
    res.append(lines(arr([V - abs(i - N // 2) for i in range(N)])))
    return res
