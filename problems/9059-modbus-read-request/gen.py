import os

from genlib import *

PID = 9059


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


def crc16_modbus(data):
    """按参数模型：输入反射、左移 poly 0x8005、init 0xFFFF、输出反射"""
    crc = 0xFFFF
    for x in data:
        crc ^= reflect(x, 8) << 8
        for _ in range(8):
            crc = ((crc << 1) ^ 0x8005) & 0xFFFF if crc & 0x8000 else (crc << 1) & 0xFFFF
    return reflect(crc, 16)


assert crc16_modbus(b"123456789") == 0x4B37


def ref(slave, start, count):
    if not (1 <= slave <= 247 and 1 <= count <= 125 and start + count <= 65536):
        return []
    body = [slave, 3, start >> 8, start & 0xFF, count >> 8, count & 0xFF]
    c = crc16_modbus(body)
    return body + [c & 0xFF, c >> 8]


def case(slave, start, count):
    return lines(slave, start, count), arr(ref(slave, start, count))


def samples():
    res = [case(1, 0, 1), case(17, 107, 3), case(0, 0, 1)]
    assert [w for _, w in res] == ["[1,3,0,0,0,1,132,10]", "[17,3,0,107,0,3,118,135]", "[]"]
    return res


def cases():
    res = [
        case(247, 65411, 125),     # 地址、数量、从机号都取上限，正好不越界
        case(247, 65412, 125),     # 越界一个
        case(1, 65535, 1),
        case(1, 65535, 2),
        case(248, 0, 1),           # 保留地址
        case(255, 100, 10),
        case(10, 0, 0),            # 数量 0
        case(10, 0, 126),          # 数量超限
        case(10, 0, 65535),
        case(2, 40000, 10),
        case(100, 256, 256),
        case(128, 4660, 100),
    ]
    for _ in range(6):
        res.append(case(random.randint(1, 247), random.randint(0, 65000), random.randint(1, 125)))
    cross_check(samples() + res)
    return [t for t, _ in res]
