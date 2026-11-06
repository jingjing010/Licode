from genlib import *


def mirror(n):
    """镜像构造法（与公式法独立的暴力参照）"""
    seq = [0]
    for k in range(n):
        seq = seq + [x | (1 << k) for x in reversed(seq)]
    return seq


def valid(seq, n):
    total = 1 << n
    if len(seq) != total or seq[0] != 0 or sorted(seq) != list(range(total)):
        return False
    return all(bin(seq[i] ^ seq[(i + 1) % total]).count("1") == 1 for i in range(total))


def samples():
    return [
        (lines(2), "[0,1,3,2]"),
        (lines(1), "[0,1]"),
    ]


def cases():
    for n in range(1, 17):
        std = [i ^ (i >> 1) for i in range(1 << n)]
        assert valid(std, n) and std == mirror(n)
    assert not valid([0, 1, 2, 3], 2) and valid([0, 2, 3, 1], 2)
    return [lines(n) for n in [3, 4, 5, 6, 7, 8, 10, 12, 13, 14, 15, 16]]
