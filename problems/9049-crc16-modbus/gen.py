import os

from genlib import *

PID = 9049


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


def reflect(x, w):
    return int(bin(x)[2:].zfill(w)[::-1], 2)


def ref_crc16_modbus(data):
    """按参数模型直接计算：输入字节反射 → 不反射的左移算法(poly 0x8005, init 0xFFFF) → 输出反射"""
    crc = 0xFFFF
    for x in data:
        crc ^= reflect(x, 8) << 8
        for _ in range(8):
            crc = ((crc << 1) ^ 0x8005) & 0xFFFF if crc & 0x8000 else (crc << 1) & 0xFFFF
    return reflect(crc, 16)


assert ref_crc16_modbus(b"123456789") == 0x4B37


def case(data):
    return lines(arr(data)), str(ref_crc16_modbus(data))


def samples():
    res = [case(list(b"123456789")), case([1, 3, 0, 0, 0, 1]), case([])]
    assert [w for _, w in res] == ["19255", "2692", "65535"]
    return res


def cases():
    c = ref_crc16_modbus([17, 3, 0, 107, 0, 3])
    res = [
        case([0]),
        case([255]),
        case([17, 3, 0, 107, 0, 3]),
        case([17, 3, 0, 107, 0, 3, c & 0xFF, c >> 8]),   # 整帧（含 CRC）再算一次结果为 0
        case([1, 6, 0, 1, 0, 23]),
        case([0] * 256),
        case([255] * 1000),
    ]
    for n in (2, 8, 100, 1000):
        res.append(case(rand_arr(n, 0, 255)))
    res.append(case(rand_arr(10**5, 0, 255)))
    res.append(case([3] * 10**5))
    cross_check(samples() + res)
    return [t for t, _ in res]
