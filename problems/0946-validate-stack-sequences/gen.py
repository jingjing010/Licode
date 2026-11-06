from genlib import *

N = 1000
XCHECK_LIMIT = 2000


def brute(pushed, popped):
    """经典判据（与模拟法无关）：把 popped 换成入栈下标序列 p，
       合法当且仅当不存在 i<j<k 使 p[j] < p[k] < p[i]（即不含 "312" 模式）"""
    n = len(pushed)
    pos = {v: i for i, v in enumerate(pushed)}
    p = [pos[v] for v in popped]
    for i in range(n):
        for j in range(i + 1, n):
            if p[j] >= p[i]:
                continue
            for k in range(j + 1, n):
                if p[j] < p[k] < p[i]:
                    return False
    return True


def expect(inp):
    import json
    a, b = (json.loads(x) for x in inp.splitlines()[:2])
    return "true" if brute(a, b) else "false"


def valid_popped(pushed):
    """随机模拟一次合法的 push/pop，得到一个合法出栈序列"""
    st, out, i = [], [], 0
    while len(out) < len(pushed):
        if i < len(pushed) and (not st or random.random() < 0.5):
            st.append(pushed[i])
            i += 1
        else:
            out.append(st.pop())
    return out


def case(a, b):
    return lines(arr(a), arr(b))


def samples():
    res = []
    for a, b, want in (([1, 2, 3, 4, 5], [4, 5, 3, 2, 1], True),
                       ([1, 2, 3, 4, 5], [4, 3, 5, 1, 2], False)):
        assert brute(a, b) == want
        res.append((case(a, b), "true" if want else "false"))
    return res


def cases():
    res = [
        case([0], [0]),
        case([1, 0], [1, 0]),
        case([1, 0], [0, 1]),
        case([2, 1, 0], [1, 2, 0]),
        case([1, 2, 3], [3, 1, 2]),
    ]
    for n in (6, 10, 30):
        a = rand_distinct(n, 0, 1000)
        res.append(case(a, valid_popped(a)))
        b = a[:]
        random.shuffle(b)
        res.append(case(a, b))
    a = rand_distinct(N, 0, 1000)
    res.append(case(a, a[::-1]))
    res.append(case(a, a))
    b = valid_popped(a)
    res.append(case(a, b))
    c = b[:]
    i = random.randrange(N - 1)
    c[i], c[i + 1] = c[i + 1], c[i]
    res.append(case(a, c))
    res.append(case(a, a[1:] + a[:1]))
    res.append(case(a, a[-1:] + a[:-1]))
    return res
