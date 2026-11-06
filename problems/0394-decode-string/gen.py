from genlib import *

MAX_OUT = 10**5


def decode(x):
    def go(i):
        out = []
        while i < len(x) and x[i] != "]":
            if x[i].isdigit():
                k = 0
                while x[i].isdigit():
                    k = k * 10 + int(x[i])
                    i += 1
                inner, i = go(i + 1)
                out.append(inner * k)
                i += 1
            else:
                out.append(x[i])
                i += 1
        return "".join(out), i
    return go(0)[0]


def samples():
    data = [
        ("3[a]2[bc]", "aaabcbc"),
        ("3[a2[c]]", "accaccacc"),
        ("2[abc]3[cd]ef", "abcabccdcdcdef"),
        ("abc3[cd]xyz", "abccdcdcdxyz"),
    ]
    for x, want in data:
        assert decode(x) == want
    return [(lines(s(x)), s(want)) for x, want in data]


def rand_enc(depth):
    parts = []
    for _ in range(random.randint(1, 3)):
        if depth > 0 and random.random() < 0.5:
            k = random.choice([1, 2, 3, 9, 10, 12, 99, 100, 300, random.randint(1, 300)])
            parts.append("%d[%s]" % (k, rand_enc(depth - 1)))
        else:
            parts.append(rand_str(random.randint(1, 3), "abcxyz"))
    return "".join(parts)


def valid(x):
    return 1 <= len(x) <= 30 and len(decode(x)) <= MAX_OUT


def cases():
    fixed = [
        "a", "abc", "1[a]", "300[a]", "2[ab]", "10[a]",
        "2[2[2[a]]]", "a2[b]c3[d]e", "3[z]2[2[y]pq4[2[jk]e1[f]]]ef",
        "300[300[a]]", "10[10[10[100[a]]]]", "300[abcdefghijklmnopqrstuv]",
        "100[leetcode]", "2[a3[b4[c5[d]]]]", "1[1[1[1[1[1[1[1[1[x]]]]]]]]]",
    ]
    res = []
    for x in fixed:
        assert valid(x), x
        res.append(lines(s(x)))
    seen = set(fixed)
    while len(res) < len(fixed) + 10:
        x = rand_enc(random.randint(1, 4))
        if valid(x) and x not in seen and any(c.isdigit() for c in x):
            seen.add(x)
            res.append(lines(s(x)))
    return res
