from genlib import *

N, V = 5 * 10**4, 5 * 10**4
XCHECK_LIMIT = 20000


def brute(a):
    best = 0
    for i in range(len(a)):
        for j in range(len(a) - 1, i + best, -1):
            if a[i] <= a[j]:
                best = j - i
                break
    return best


def expect(inp):
    import json
    return str(brute(json.loads(inp.splitlines()[0])))


def samples():
    res = []
    for a, want in (([6, 0, 8, 2, 1, 5], 4), ([9, 8, 1, 0, 1, 9, 4, 0, 4, 1], 7)):
        assert brute(a) == want
        res.append((lines(arr(a)), str(want)))
    return res


def cases():
    res = [
        lines(arr([1, 0])),
        lines(arr([0, 1])),
        lines(arr([3, 3])),
        lines(arr([5, 4, 3, 2, 1])),
        lines(arr([2, 1, 3, 0, 1])),
    ]
    for n, hi in ((10, 10), (100, 50), (1000, V)):
        res.append(lines(arr(rand_arr(n, 0, hi))))
    res.append(lines(arr(list(range(N, 0, -1)))))
    res.append(lines(arr([7] * N)))
    res.append(lines(arr(rand_arr(N, 0, V))))
    a = list(range(V, V - N, -1))
    a[N // 2] = V
    res.append(lines(arr(a)))
    res.append(lines(arr([V - i if i % 2 == 0 else i // 2 for i in range(N)])))
    res.append(lines(arr(list(range(N - 1, -1, -1))[: N - 1] + [N // 3])))
    return res
