from genlib import *

AL = "abcdefghijklmnopqrstuvwxyz"


def samples():
    return [
        (lines(carr("cfj"), s("a")), '"c"'),
        (lines(carr("cfj"), s("c")), '"f"'),
        (lines(carr("xxyy"), s("z")), '"x"'),
    ]


def brute(letters, t):
    for c in letters:
        if c > t:
            return c
    return letters[0]


def binary(letters, t):
    lo, hi = 0, len(letters)
    while lo < hi:
        mid = (lo + hi) // 2
        if letters[mid] <= t:
            lo = mid + 1
        else:
            hi = mid
    return letters[lo] if lo < len(letters) else letters[0]


def rand_letters(n, alphabet=AL):
    while True:
        a = sorted(random.choice(alphabet) for _ in range(n))
        if len(set(a)) >= 2:
            return "".join(a)


def cases():
    res = [
        ("ab", "a"),
        ("ab", "b"),
        ("az", "y"),
        ("az", "z"),
        ("aaaaz", "a"),
        ("eeeeeeeennnn", "e"),
        ("eeeeeeeennnn", "n"),
    ]
    for n in (10, 100, 1000):
        res.append((rand_letters(n), random.choice(AL)))
    N = 10**4
    res.append(("a" * (N - 1) + "b", "a"))
    res.append(("a" + "z" * (N - 1), "z"))
    res.append((rand_letters(N), random.choice(AL)))
    res.append((rand_letters(N, "mn"), "m"))
    for letters, t in res:
        assert len(set(letters)) >= 2
        assert brute(letters, t) == binary(letters, t)
    for _ in range(300):
        letters = rand_letters(random.randint(2, 12), "abcdef")
        t = random.choice("abcdefg")
        assert brute(letters, t) == binary(letters, t)
    return [lines(carr(a), s(t)) for a, t in res]
