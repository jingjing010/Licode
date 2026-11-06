from genlib import *


def valid(t):
    bal = 0
    for c in t:
        bal += 1 if c == "(" else -1
        if bal < 0:
            return False
    return bal == 0


def brute(t):
    n = len(t)
    return max([j - i for i in range(n) for j in range(i + 2, n + 1, 2) if valid(t[i:j])], default=0)


def fast(t):
    st, best = [-1], 0
    for i, c in enumerate(t):
        if c == "(":
            st.append(i)
        else:
            st.pop()
            if not st:
                st.append(i)
            else:
                best = max(best, i - st[-1])
    return best


def rand_valid(n):
    """随机生成长度为 n（偶数）的合法括号串"""
    out, open_left, bal = [], n // 2, 0
    for _ in range(n):
        if open_left and (bal == 0 or random.random() < 0.5):
            out.append("(")
            open_left -= 1
            bal += 1
        else:
            out.append(")")
            bal -= 1
    return "".join(out)


def samples():
    return [
        (lines(s("(()")), "2"),
        (lines(s(")()())")), "4"),
        (lines(s("")), "0"),
    ]


def cases():
    for _ in range(300):
        t = rand_str(random.randint(0, 14), "()")
        assert brute(t) == fast(t)
    N = 3 * 10**4
    return [
        lines(s("(")),
        lines(s(")")),
        lines(s("()")),
        lines(s(")(")),
        lines(s("()(()")),
        lines(s("()(())")),
        lines(s("(()))())(")),
        lines(s(rand_str(20, "()"))),
        lines(s(rand_str(1000, "()"))),
        lines(s("(" * N)),
        lines(s("()" * (N // 2))),
        lines(s("(" * (N // 2) + ")" * (N // 2))),
        lines(s(rand_valid(N))),
        lines(s(rand_valid(14000) + ")" + rand_valid(16000)[:-1])),
        lines(s(rand_str(N, "()"))),
        lines(s(")" + rand_valid(N - 2) + "(")),
    ]
