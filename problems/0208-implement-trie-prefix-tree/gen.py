from genlib import *
import json


def samples():
    return [
        (lines(sarr(["Trie", "insert", "search", "search", "startsWith", "insert", "search"]),
               "[[],[\"apple\"],[\"apple\"],[\"app\"],[\"app\"],[\"app\"],[\"app\"]]"),
         "[null,null,true,false,true,null,true]"),
    ]


def fmt(ops, args):
    return lines(sarr(["Trie"] + ops), "[" + ",".join(["[]"] + [sarr([a]) for a in args]) + "]")


def rand_ops(cnt, make_word, p_insert=0.4):
    ops, args, words = [], [], []
    for _ in range(cnt):
        r = random.random()
        if r < p_insert or not words:
            w = make_word()
            words.append(w)
            ops.append("insert")
            args.append(w)
            continue
        op = random.choice(["search", "startsWith"])
        k = random.random()
        if k < 0.4:
            w = random.choice(words)                          # 插入过的单词
        elif k < 0.7:
            w = random.choice(words)
            w = w[:random.randint(1, len(w))]                 # 某个单词的前缀
        else:
            w = make_word()                                   # 随机串
        ops.append(op)
        args.append(w)
    return fmt(ops, args)


def cases():
    res = [
        fmt(["search", "startsWith"], ["a", "a"]),
        fmt(["insert", "search", "startsWith", "search"], ["a", "a", "a", "b"]),
        fmt(["insert", "insert", "search", "search", "startsWith", "startsWith"],
            ["abc", "abc", "abc", "ab", "abcd", "ab"]),
        fmt(["insert", "insert", "search", "search", "search", "startsWith"],
            ["apple", "apply", "appl", "apple", "applz", "appl"]),
        fmt(["insert", "search", "startsWith", "startsWith"], ["z" * 2000, "z" * 1999, "z" * 2000, "z" * 1000]),
    ]
    res.append(rand_ops(50, lambda: rand_str(random.randint(1, 4), "ab")))
    res.append(rand_ops(1000, lambda: rand_str(random.randint(1, 6), "abc")))
    res.append(rand_ops(30000, lambda: rand_str(random.randint(1, 8), "abc"), 0.3))
    res.append(rand_ops(30000, lambda: rand_str(random.randint(1, 12)), 0.5))
    res.append(rand_ops(20000, lambda: rand_str(random.randint(15, 25), "abcdefghij"), 0.5))
    P = rand_str(1990)
    res.append(rand_ops(700, lambda: P + rand_str(random.randint(1, 10), "xyz"), 0.4))
    res.append(rand_ops(30000, lambda: rand_str(random.randint(1, 3)), 0.2))
    return res


def brute(text):
    ls = text.strip().splitlines()
    ops = json.loads(ls[0])
    args = json.loads(ls[1])
    words, pre, out = set(), set(), []
    for op, a in zip(ops, args):
        if op == "Trie":
            words, pre = set(), set()
            out.append("null")
        elif op == "insert":
            words.add(a[0])
            for i in range(1, len(a[0]) + 1):
                pre.add(a[0][:i])
            out.append("null")
        elif op == "search":
            out.append(b(a[0] in words))
        else:
            out.append(b(a[0] in pre))
    return "[" + ",".join(out) + "]"


if __name__ == "__main__":
    # 交叉验证：先 python tools/build.py 208，再 PYTHONPATH=tools python gen.py
    import glob, os
    d = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tests")
    for f in sorted(glob.glob(os.path.join(d, "*.in"))):
        got = open(f[:-3] + ".out", encoding="utf-8").read().strip()
        assert got == brute(open(f, encoding="utf-8").read()), f
    print("brute ok")
