from genlib import *

XCHECK_LIMIT = 10**5


def brute(t):
    """不断删掉相邻的 "()"，剩下的每个括号都要补一个"""
    while "()" in t:
        t = t.replace("()", "")
    return len(t)


def expect(inp):
    import json
    return str(brute(json.loads(inp.splitlines()[0])))


def samples():
    res = []
    for t, want in (("())", 1), ("(((", 3)):
        assert brute(t) == want
        res.append((lines(s(t)), str(want)))
    return res


def cases():
    res = [
        lines(s("(")),
        lines(s(")")),
        lines(s("()")),
        lines(s(")(")),
        lines(s("()))((")),
        lines(s(")" * 1000)),
        lines(s("(" * 500 + ")" * 500)),
        lines(s(")" * 500 + "(" * 500)),
        lines(s("()" * 500)),
    ]
    for n in (10, 50, 200, 1000, 1000):
        res.append(lines(s(rand_str(n, "()"))))
    res.append(lines(s("".join(random.choice(["(", "(", ")"]) for _ in range(1000)))))
    return res
