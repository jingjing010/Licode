import os
import zlib

from genlib import *

PID = 9050


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


def ref_bitwise(data):
    crc = 0xFFFFFFFF
    for x in data:
        crc ^= x
        for _ in range(8):
            crc = (crc >> 1) ^ 0xEDB88320 if crc & 1 else crc >> 1
    return crc ^ 0xFFFFFFFF


assert ref_bitwise(b"123456789") == 0xCBF43926 == zlib.crc32(b"123456789")


def case(data):
    data = bytes(data)
    want = zlib.crc32(data) & 0xFFFFFFFF
    if len(data) <= 5000:
        assert want == ref_bitwise(data)
    return lines(arr(list(data))), str(want)


def samples():
    res = [case(b"123456789"), case(b"a"), case(b"")]
    assert [w for _, w in res] == ["3421780262", "3904355907", "0"]
    return res


def cases():
    res = [
        case([0]),
        case([255]),
        case([0, 0, 0, 0]),
        case([255] * 4),
        case(b"The quick brown fox jumps over the lazy dog"),
        case(bytes(range(256))),
    ]
    for n in (3, 16, 255, 4096):
        res.append(case(rand_arr(n, 0, 255)))
    res.append(case(rand_arr(2 * 10**5, 0, 255)))
    res.append(case([0xFF] * (2 * 10**5)))
    cross_check(samples() + res)
    return [t for t, _ in res]
