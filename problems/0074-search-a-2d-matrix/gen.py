from genlib import *

EX = [[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]]


def samples():
    return [
        (lines(mat(EX), 3), "true"),
        (lines(mat(EX), 13), "false"),
    ]


def make(m, n, dup=False):
    """生成满足题意的矩阵：每行非递减，且每行第一个 > 上一行最后一个"""
    vals = sorted(rand_distinct(m * n, -10**4, 10**4))
    g = [vals[i * n:(i + 1) * n] for i in range(m)]
    if dup:
        for r in g:
            for j in range(1, n):
                if random.random() < 0.4:
                    r[j] = r[j - 1]
    return g


def brute(g, t):
    return any(t in r for r in g)


def case(g, t):
    return lines(mat(g), t)


def cases():
    res = [
        case([[1]], 1),
        case([[1]], 2),
        case([[1, 3]], 3),
        case([[1], [3]], 2),
        case([[-10000, 10000]], -10000),
        case(make(1, 100), 10**4),
        case(make(100, 1), -10**4),
    ]
    for (m, n) in ((3, 4), (10, 10), (30, 50)):
        g = make(m, n, dup=True)
        res.append(case(g, random.choice(random.choice(g))))
        flat = {x for r in g for x in r}
        t = random.randint(-10**4, 10**4)
        while t in flat:
            t = random.randint(-10**4, 10**4)
        res.append(case(g, t))
    g = make(100, 100)
    res.append(case(g, g[99][99]))
    res.append(case(g, g[0][0]))
    flat = {x for r in g for x in r}
    t = next(x for x in range(g[50][0], 10**4) if x not in flat)
    res.append(case(g, t))
    return res
