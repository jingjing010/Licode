from genlib import *

BIG = 2**31 - 1


def brute(coins, amount):
    """BFS：按硬币个数分层"""
    if amount == 0:
        return 0
    seen, layer, steps = {0}, [0], 0
    while layer:
        steps += 1
        nxt = []
        for v in layer:
            for c in coins:
                w = v + c
                if w == amount:
                    return steps
                if w < amount and w not in seen:
                    seen.add(w)
                    nxt.append(w)
        layer = nxt
    return -1


def fast(coins, amount):
    INF = amount + 1
    dp = [0] + [INF] * amount
    for i in range(1, amount + 1):
        for c in coins:
            if c <= i and dp[i - c] + 1 < dp[i]:
                dp[i] = dp[i - c] + 1
    return -1 if dp[amount] >= INF else dp[amount]


def samples():
    return [
        (lines(arr([1, 2, 5]), 11), "3"),
        (lines(arr([2]), 3), "-1"),
        (lines(arr([1]), 0), "0"),
    ]


def cases():
    for _ in range(300):
        coins = rand_distinct(random.randint(1, 4), 1, 15)
        amount = random.randint(0, 60)
        assert brute(coins, amount) == fast(coins, amount)
    return [
        lines(arr([1]), 1),
        lines(arr([2]), 1),
        lines(arr([1, 3, 4]), 6),
        lines(arr([186, 419, 83, 408]), 6249),
        lines(arr([BIG]), 2),
        lines(arr([BIG, 1, 2]), 10000),
        lines(arr([2, 4, 6, 8]), 9999),
        lines(arr([7, 11]), 10000),
        lines(arr([1]), 10000),
        lines(arr([10000]), 10000),
        lines(arr(rand_distinct(12, 1, 100)), 10000),
        lines(arr(rand_distinct(12, 50, 500)), 9973),
        lines(arr([BIG, 4999, 5003]), 10000),
        lines(arr(rand_distinct(5, 1, 30)), random.randint(1, 500)),
    ]
