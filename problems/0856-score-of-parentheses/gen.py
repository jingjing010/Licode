from genlib import *


def brute(t):
    """按定义递归：拆成若干原语，每个原语 (A) 的分数是 1（A 为空）或 2*score(A)"""
    if not t:
        return 0
    total, bal, start = 0, 0, 0
    for i, c in enumerate(t):
        bal += 1 if c == "(" else -1
        if bal == 0:
            inner = t[start + 1:i]
            total += 1 if not inner else 2 * brute(inner)
            start = i + 1
    return total


def expect(inp):
    import json
    return str(brute(json.loads(inp.splitlines()[0])))


def rand_balanced(n):
    """随机生成长度为 n（偶数）的平衡括号串"""
    res, opened, closed, half = [], 0, 0, n // 2
    while len(res) < n:
        if opened < half and (opened == closed or random.random() < 0.5):
            res.append("(")
            opened += 1
        else:
            res.append(")")
            closed += 1
    return "".join(res)


def samples():
    res = []
    for t, want in (("()", 1), ("(())", 2), ("()()", 2), ("(()(()))", 6)):
        assert brute(t) == want
        res.append((lines(s(t)), str(want)))
    return res


def cases():
    res = [
        lines(s("(" * 25 + ")" * 25)),
        lines(s("(" * 24 + "()" + ")" * 24)),
        lines(s("()" * 25)),
        lines(s("(" * 20 + "()" * 5 + ")" * 20)),
        lines(s("((()))(())()")),
        lines(s("(" * 23 + "()()" + ")" * 23)),
    ]
    for n in (6, 10, 20, 30, 40, 50, 50, 50, 50):
        res.append(lines(s(rand_balanced(n))))
    return res
