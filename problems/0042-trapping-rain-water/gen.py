from genlib import *


def samples():
    return [
        (lines(arr([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1])), "6"),
        (lines(arr([4, 2, 0, 3, 2, 5])), "9"),
    ]


def brute(h):
    n, ans = len(h), 0
    for i in range(n):
        ans += min(max(h[:i + 1]), max(h[i:])) - h[i]
    return ans


def fast(h):
    l, r, lm, rm, ans = 0, len(h) - 1, 0, 0, 0
    while l < r:
        lm, rm = max(lm, h[l]), max(rm, h[r])
        if lm < rm:
            ans += lm - h[l]
            l += 1
        else:
            ans += rm - h[r]
            r -= 1
    return ans


for _ in range(300):
    _h = rand_arr(random.randint(1, 30), 0, 10)
    assert brute(_h) == fast(_h)


def cases():
    N, H = 2 * 10**4, 10**5
    res = [
        lines(arr([5])),
        lines(arr([2, 0])),
        lines(arr([3, 0, 3])),
        lines(arr([1, 2, 3, 4, 5])),
        lines(arr([5, 4, 3, 2, 1])),
        lines(arr([0, 0, 0, 0])),
        lines(arr([5, 2, 1, 2, 1, 5])),
    ]
    for n in (20, 200, 2000):
        res.append(lines(arr(rand_arr(n, 0, 50))))
    res.append(lines(arr(rand_arr(N, 0, H))))
    res.append(lines(arr([H] + [0] * (N - 2) + [H])))
    valley = [abs(i - N // 2) * 10 for i in range(N)]
    res.append(lines(arr(valley)))
    res.append(lines(arr([H if i % 2 == 0 else 0 for i in range(N)])))
    return res
