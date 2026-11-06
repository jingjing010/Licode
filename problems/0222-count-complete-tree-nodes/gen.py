from genlib import *


def parse(line):
    line = line.strip()[1:-1].strip()
    if not line:
        return []
    return [None if t.strip() == "null" else int(t) for t in line.split(",")]


def brute(inp):
    """完全二叉树的层序表示没有 null，直接数非空值的个数"""
    return str(sum(1 for v in parse(inp.split("\n")[0]) if v is not None))


def complete(n, lo=0, hi=5 * 10**4):
    return lines(tree(rand_arr(n, lo, hi)))


def samples():
    res = [
        (lines("[1,2,3,4,5,6]"), "6"),
        (lines("[]"), "0"),
        (lines("[1]"), "1"),
    ]
    for inp, want in res:
        assert brute(inp) == want
    return res


def cases():
    return [
        complete(2),
        complete(3),
        complete(4),
        complete(7),
        complete(8),
        complete(100),
        complete(1023),
        complete(1024),
        complete(32767),
        complete(32768),
        complete(40000),
        complete(5 * 10**4),
        complete(5 * 10**4, 0, 0),
        complete(49999),
    ]


if __name__ == "__main__":
    import glob
    import os
    here = os.path.dirname(os.path.abspath(__file__))
    for f in sorted(glob.glob(os.path.join(here, "tests", "*.in"))):
        with open(f, encoding="utf-8") as fi:
            inp = fi.read()
        with open(f[:-3] + ".out", encoding="utf-8") as fo:
            want = fo.read().strip()
        assert brute(inp) == want, os.path.basename(f)
    print("brute check ok")
