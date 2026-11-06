from genlib import *

V = 10**4
N = 1000


def fmt(nodes):
    return "[" + ",".join("[%d,%s]" % (v, "null" if r is None else r) for v, r in nodes) + "]"


def rnd_list(n, p_null=0.2, lo=-V, hi=V):
    return [(random.randint(lo, hi), None if random.random() < p_null else random.randrange(n))
            for _ in range(n)]


def samples():
    return [
        (lines(fmt([(7, None), (13, 0), (11, 4), (10, 2), (1, 0)])), "[[7,null],[13,0],[11,4],[10,2],[1,0]]"),
        (lines(fmt([(1, 1), (2, 1)])), "[[1,1],[2,1]]"),
        (lines(fmt([(3, None), (3, 0), (3, None)])), "[[3,null],[3,0],[3,null]]"),
    ]


def cases():
    return [
        lines("[]"),
        lines(fmt([(5, None)])),
        lines(fmt([(5, 0)])),
        lines(fmt([(-1, 1), (-1, 0)])),
        lines(fmt(rnd_list(10))),
        lines(fmt(rnd_list(50, 0.0))),
        lines(fmt(rnd_list(200, 1.0))),
        lines(fmt(rnd_list(N))),
        lines(fmt([(random.randint(-V, V), i) for i in range(N)])),
        lines(fmt([(random.randint(-V, V), N - 1 - i) for i in range(N)])),
        lines(fmt([(0, 0)] * N)),
        lines(fmt(rnd_list(N, 0.0, -V, -V))),
        lines(fmt(rnd_list(N, 0.5, V, V))),
        lines(fmt(rnd_list(N - 1, 0.1))),
    ]
