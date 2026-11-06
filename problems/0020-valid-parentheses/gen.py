from genlib import *

PAIR = {")": "(", "]": "[", "}": "{"}


def brute(x):
    st = []
    for c in x:
        if c in "([{":
            st.append(c)
        elif not st or st.pop() != PAIR[c]:
            return False
    return not st


def samples():
    data = [("()", True), ("()[]{}", True), ("(]", False), ("([])", True)]
    for x, want in data:
        assert brute(x) == want
    return [(lines(s(x)), b(want)) for x, want in data]


def valid(n):
    """随机生成长度为 n（偶数）的有效括号串"""
    out, st = [], []
    while len(out) < n:
        rest = n - len(out)
        if st and (rest == len(st) or random.random() < 0.5):
            out.append({"(": ")", "[": "]", "{": "}"}[st.pop()])
        else:
            c = random.choice("([{")
            st.append(c)
            out.append(c)
    return "".join(out)


def mutate(x):
    i = random.randrange(len(x))
    c = random.choice([ch for ch in "()[]{}" if ch != x[i]])
    return x[:i] + c + x[i + 1:]


def cases():
    fixed = ["(", ")", "]", "((", "){", "([)]", "{[]}", "(((())))", "(()", "())",
             "[(])", "{}{}{}", "((((((((((", "))))))))))"]
    res = [lines(s(x)) for x in fixed]
    for n in (10, 100, 1000):
        v = valid(n)
        res.append(lines(s(v)))
        res.append(lines(s(mutate(v))))
    big = valid(10**4)
    res.append(lines(s(big)))
    res.append(lines(s(mutate(big))))
    res.append(lines(s("(" * 5000 + ")" * 5000)))
    res.append(lines(s("(" * 5000 + ")" * 4999 + "]")))
    res.append(lines(s("[" * 9999 + "]")))
    res.append(lines(s("{}" * 5000)))
    for t in res:
        x = t.strip()[1:-1]
        assert 1 <= len(x) <= 10**4
    return res
