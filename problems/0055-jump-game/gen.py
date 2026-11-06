from genlib import *


def brute(a):
    n = len(a)
    reach = [False] * n
    reach[0] = True
    for i in range(n):
        if reach[i]:
            for j in range(i + 1, min(n, i + a[i] + 1)):
                reach[j] = True
    return reach[-1]


def fast(a):
    far = 0
    for i, x in enumerate(a):
        if i > far:
            return False
        far = max(far, i + x)
    return True


def samples():
    return [
        (lines(arr([2, 3, 1, 1, 4])), "true"),
        (lines(arr([3, 2, 1, 0, 4])), "false"),
    ]


def cases():
    for _ in range(300):
        a = rand_arr(random.randint(1, 10), 0, 3)
        assert brute(a) == fast(a)
    n = 10**4
    big_true = [1] * n
    big_false = [1] * n
    big_false[n // 2] = 0
    stair = [max(0, (n - 2) - i) for i in range(n)]  # 每个位置最远都只能到 n-2，到不了终点
    res = [
        lines(arr([0])),
        lines(arr([5])),
        lines(arr([0, 1])),
        lines(arr([1, 0])),
        lines(arr([2, 0, 0])),
        lines(arr([1, 1, 0, 1])),
        lines(arr(rand_arr(10, 0, 3))),
        lines(arr(rand_arr(100, 0, 3))),
        lines(arr(big_true)),
        lines(arr(big_false)),
        lines(arr(stair)),
        lines(arr([10**5] + [0] * (n - 1))),
    ]
    # 大规模随机：一真一假
    while True:
        a = rand_arr(n, 0, 3)
        a[0] = 3
        if fast(a):
            res.append(lines(arr(a)))
            break
        a = [random.randint(1, 4) if random.random() < 0.9 else 0 for _ in range(n)]
        if fast(a):
            res.append(lines(arr(a)))
            break
    a = [random.randint(1, 5) for _ in range(n)]
    for k in range(5):
        a[n - 2 - k] = k  # 倒数几个位置都恰好跳到倒数第 2 个，且那里是 0
    assert not fast(a)
    res.append(lines(arr(a)))
    return res
