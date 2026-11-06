from genlib import *

LO, HI = -2**31, 2**31 - 1


def tdiv(a, b):
    q = abs(a) // abs(b)
    return q if (a >= 0) == (b > 0) else -q


def apply(op, a, b):
    if op == "+":
        return a + b
    if op == "-":
        return a - b
    if op == "*":
        return a * b
    return tdiv(a, b)


def ref(tokens):
    st = []
    for t in tokens:
        if t in ("+", "-", "*", "/"):
            b = st.pop()
            a = st.pop()
            r = apply(t, a, b)
            assert LO <= r <= HI
            st.append(r)
        else:
            st.append(int(t))
    assert len(st) == 1
    return st[0]


def try_op(st, ops):
    """在栈顶两个数上尝试运算符（按给定顺序），成功则返回运算符"""
    a, b = st[-2], st[-1]
    for op in ops:
        if op == "/" and b == 0:
            continue
        r = apply(op, a, b)
        if LO <= r <= HI:
            st.pop()
            st.pop()
            st.append(r)
            return op
    return None


def make(n, lo=-200, hi=200, num_p=0.5, ops="+-*/"):
    """生成恰好 n 个记号（n 为奇数）的合法逆波兰表达式，保证中间结果在 32 位内"""
    assert n % 2 == 1
    tokens, st = [], []
    nums_left = (n + 1) // 2
    while len(tokens) < n:
        ops_left = n - len(tokens) - nums_left
        can_num = nums_left > 0
        can_op = len(st) >= 2 and ops_left > 0
        if can_num and (not can_op or random.random() < num_p):
            v = random.randint(lo, hi)
            tokens.append(str(v))
            st.append(v)
            nums_left -= 1
        else:
            order = "".join(random.sample(ops, len(ops)))
            op = try_op(st, order + "/+")
            assert op is not None
            tokens.append(op)
    return tokens


def case(tokens):
    return lines(sarr(tokens))


def samples():
    data = [
        (["2", "1", "+", "3", "*"], 9),
        (["4", "13", "5", "/", "+"], 6),
        (["10", "6", "9", "3", "+", "-11", "*", "/", "*", "17", "+", "5", "+"], 22),
    ]
    out = []
    for t, want in data:
        assert ref(t) == want
        out.append((case(t), str(want)))
    return out


def cases():
    fixed = [
        ["0"],
        ["-200"],
        ["200", "-200", "-"],
        ["-7", "2", "/"],
        ["7", "-2", "/"],
        ["0", "-5", "/"],
        ["200", "200", "*", "200", "*", "-200", "*"],
    ]
    for t in fixed:
        ref(t)
    res = [case(t) for t in fixed]
    for n in (11, 51, 301):
        res.append(case(make(n)))
    for t in (make(9999), make(9999, num_p=0.8), make(9999, num_p=0.3, ops="*/")):
        ref(t)
        res.append(case(t))
    return res
