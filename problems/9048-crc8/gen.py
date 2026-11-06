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


def ref(data):
    """多项式长除法的直接实现：把整段数据看成一个大整数，后面补 8 个 0 再模 2 除以 0x107"""
    v = int.from_bytes(bytes(data), "big") << 8 if data else 0
    poly = 0x107
    while v.bit_length() > 8:
        v ^= poly << (v.bit_length() - 9)
    return v


def ref_bitwise(data):
    crc = 0
    for x in data:
        crc ^= x
        for _ in range(8):
            crc = ((crc << 1) ^ 0x07) & 0xFF if crc & 0x80 else (crc << 1) & 0xFF
    return crc


assert ref(b"123456789") == 0xF4 == ref_bitwise(b"123456789")


def case(data):
    data = list(data)
    want = ref_bitwise(data)
    if len(data) <= 2000:
        assert want == ref(data)
    return lines(arr(data)), str(want)


def samples():
    res = [case(b"123456789"), case([1]), case([])]
    assert [w for _, w in res] == ["244", "7", "0"]
    return res


def cases():
    res = [
        case([0]),
        case([255]),
        case([0x80]),
        case([0] * 100),
        case([255] * 1000),
        case(b"Hello, embedded world!"),
        case([0x12, 0x34]),
        case(list(b"123456789") + [0xF4]),   # 数据 + 自身 CRC，再算一次结果为 0
    ]
    for n in (2, 10, 100, 1000):
        res.append(case(rand_arr(n, 0, 255)))
    res.append(case(rand_arr(10**5, 0, 255)))
    res.append(case([250] * 10**5))
    cross_check(samples() + res)
    return [t for t, _ in res]
