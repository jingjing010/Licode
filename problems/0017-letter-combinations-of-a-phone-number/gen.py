from genlib import *
import itertools
import json

MAP = {"2": "abc", "3": "def", "4": "ghi", "5": "jkl", "6": "mno", "7": "pqrs", "8": "tuv", "9": "wxyz"}


def samples():
    return [
        (lines(s("23")), sarr(["ad", "ae", "af", "bd", "be", "bf", "cd", "ce", "cf"])),
        (lines(s("")), "[]"),
        (lines(s("2")), sarr(["a", "b", "c"])),
    ]


def cases():
    res = [lines(s(x)) for x in ["9", "7", "79", "22", "234", "777", "2345", "7979", "9999", "5678", "8642"]]
    for n in (3, 4):
        res.append(lines(s(rand_str(n, "23456789"))))
    return res


def brute(text):
    d = json.loads(text.strip().splitlines()[0])
    if not d:
        return "[]"
    return sarr(sorted("".join(p) for p in itertools.product(*[MAP[c] for c in d])))


if __name__ == "__main__":
    # 交叉验证：先 python tools/build.py 17，再 PYTHONPATH=tools python gen.py
    import glob, os
    dd = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tests")
    for f in sorted(glob.glob(os.path.join(dd, "*.in"))):
        got = open(f[:-3] + ".out", encoding="utf-8").read().strip()
        assert got == brute(open(f, encoding="utf-8").read()), f
    print("brute ok")
