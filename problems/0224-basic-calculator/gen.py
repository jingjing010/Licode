from genlib import *

LO, HI = -2**31, 2**31 - 1


def ref(expr):
    """括号展开法；同时检查所有运行中的计算都在 32 位内"""
    ops, sign, ret, i, n = [1], 1, 0, 0, len(expr)
    while i < n:
        c = expr[i]
        if c == " ":
            i += 1
        elif c == "+":
            sign = ops[-1]
            i += 1
        elif c == "-":
            sign = -ops[-1]
            i += 1
        elif c == "(":
            ops.append(sign)
            i += 1
        elif c == ")":
            ops.pop()
            i += 1
        else:
            j = i
            while j < n and expr[j].isdigit():
                j += 1
            num = int(expr[i:j])
            assert num <= HI
            ret += sign * num
            assert LO <= ret <= HI
            i = j
    return ret


def make(target_len, maxnum=1000, paren_p=0.25, close_p=0.3, space_p=0.1, neg_p=0.2):
    """随机生成合法表达式：一元 '-' 只出现在开头或 '(' 之后，'+' 不作一元运算"""
    out, depth, length = [], 0, 0

    def put(tok):
        nonlocal length
        if random.random() < space_p:
            tok = " " + tok
        out.append(tok)
        length += len(tok)

    while True:
        # 操作数位置：可在开头或 '(' 后加一元负号
        prev = out[-1].strip() if out else "("
        if prev == "(" and random.random() < neg_p:
            put("-")
        while random.random() < paren_p and length + depth < target_len:
            put("(")
            depth += 1
            if random.random() < neg_p:
                put("-")
        put(str(random.randint(0, maxnum)))
        while depth > 0 and random.random() < close_p:
            put(")")
            depth -= 1
        if length + depth >= target_len:
            break
        put(random.choice("+-"))
    put(")" * depth)
    expr = "".join(out)
    if random.random() < 0.5:
        expr = " " + expr + " "
    return expr


def case(e):
    return lines(s(e))


def samples():
    data = [("1 + 1", 2), (" 2-1 + 2 ", 3), ("(1+(4+5+2)-3)+(6+8)", 23)]
    out = []
    for e, want in data:
        assert ref(e) == want
        out.append((case(e), str(want)))
    return out


def cases():
    fixed = [
        "0",
        "-1",
        "-(2 + 3)",
        "1-(     -2)",
        "- (3 + (4 + 5))",
        "2147483647",
        "-2147483647 + 0 - 1",
        "2147483647 - (2147483647 - 5)",
        "(((((((((7)))))))))",
        "1 - (2 - (3 - (4 - (5 - 6))))",
    ]
    for e in fixed:
        ref(e)
    for _ in range(300):
        e = make(30, maxnum=50)
        assert ref(e) == eval(e)
    exprs = list(fixed)
    exprs.append(make(60))
    exprs.append(make(500))
    exprs.append(make(299000, maxnum=10000, space_p=0.05))
    exprs.append(make(299000, maxnum=100, paren_p=0.6, close_p=0.15))
    d = 99990
    exprs.append("(" * d + "1" + ")" * d)
    exprs.append("-(" * (d // 2) + "1" + ")" * (d // 2))
    exprs.append("-1" + " + 1 - 1" * 37000)
    for e in exprs[len(fixed):]:
        assert 1 <= len(e) <= 3 * 10**5
        ref(e)
    return [case(e) for e in exprs]
