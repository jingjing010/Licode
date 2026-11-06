from genlib import *

TRAFFIC = [[1, 3, -1], [2, 3, -1], [0, 3, -1], [-1, -1, 0]]


def ref(table, s, events):
    out = []
    for e in events:
        if table[s][e] != -1:
            s = table[s][e]
        out.append(s)
    return out


def rand_table(ns, ne, p_ignore=0.3):
    return [[-1 if random.random() < p_ignore else random.randrange(ns) for _ in range(ne)] for _ in range(ns)]


def samples():
    s = [
        (TRAFFIC, 0, [0, 0, 0, 0, 1, 0, 2], "[1,2,0,1,3,3,0]"),
        (TRAFFIC, 2, [2, 1, 2], "[2,3,0]"),
    ]
    for t, init, ev, want in s:
        assert arr(ref(t, init, ev)) == want
    return [(lines(mat(t), init, arr(ev)), want) for t, init, ev, want in s]


def cases():
    res = [
        lines(mat([[-1]]), 0, arr([0, 0, 0])),
        lines(mat([[0]]), 0, arr([0])),
        lines(mat([[1, -1], [-1, 0]]), 1, arr([0, 0, 1, 1, 0])),
        lines(mat(TRAFFIC), 3, arr([0, 1, 0, 1, 2, 0, 0, 0])),
        lines(mat(TRAFFIC), 0, arr(rand_arr(200, 0, 2))),
    ]
    for ns, ne, n in ((3, 2, 50), (10, 5, 1000), (50, 20, 5000)):
        res.append(lines(mat(rand_table(ns, ne)), random.randrange(ns), arr(rand_arr(n, 0, ne - 1))))
    res.append(lines(mat(rand_table(50, 20, 0.1)), 0, arr(rand_arr(10**5, 0, 19))))
    res.append(lines(mat(rand_table(50, 20, 0.9)), 49, arr(rand_arr(10**5, 0, 19))))
    res.append(lines(mat(TRAFFIC), 0, arr([0] * 10**5)))
    return res
