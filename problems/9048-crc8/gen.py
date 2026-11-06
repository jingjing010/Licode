import os

from genlib import *

PID = 9048


def cross_check(pairs):
    """用 solution.c 实际跑一遍全部输入，和 Python 对照解逐个比对"""
    import judge
    prob = judge.get_problem(PID)
    wd = judge._workdir()
    try:
        with open(os.path.join(prob["dir"], "solution.c"), encoding="utf-8") as f:
            ok, err, _, _ = judge.compile_code(prob, f.read(), wd)
        assert ok, err
        exe = os.path.join(wd, "main.exe" if os.name == "nt" else "main")
        for k, (text, want) in enumerate(pairs, 1):
            r = judge.run_one(exe, text, 5000)
            assert r["status"] == "OK", (k, r["status"])
            assert judge.normalize(r["stdout"]) == want, "第 %d 个测试与对照解不一致" % k
    finally:
        judge._cleanup(wd)


def ref_crc8(data):
    """按定义做模 2 长除法（逐位移入数据，末尾补 8 个 0），余数即 CRC"""
    reg = 0
    bits = [(x >> k) & 1 for x in data for k in range(7, -1, -1)] + [0] * 8
    for bit in bits:
        top = reg >> 7
        reg = ((reg << 1) | bit) & 0xFF
        if top:
            reg ^= 0x07
    return reg


assert ref_crc8(b"123456789") == 0xF4


def case(data):
    return lines(arr(data)), str(ref_crc8(data))


def samples():
    res = [case(list(b"123456789")), case([1]), case([])]
    assert [w for _, w in res] == ["244", "7", "0"]
    return res


def cases():
    res = [
        case([0]),
        case([255]),
        case([0] * 100),
        case([255] * 1000),
        case(list(b"Hello, embedded world!")),
        case([0x80]),
        case(list(b"123456789") + [0xF4]),   # 数据 + 自身 CRC，结果应为 0
    ]
    for n in (2, 10, 100, 1000):
        res.append(case(rand_arr(n, 0, 255)))
    res.append(case(rand_arr(10**5, 0, 255)))
    res.append(case([250] * 10**5))
    cross_check(samples() + res)
    return [t for t, _ in res]
