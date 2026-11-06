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


def ref_crc32(data):
    """Python 标准库 zlib.crc32 正是 CRC-32/ISO-HDLC"""
    return zlib.crc32(bytes(data)) & 0xFFFFFFFF


assert ref_crc32(b"123456789") == 0xCBF43926


def case(data):
    return lines(arr(data)), str(ref_crc32(data))


def samples():
    res = [case(list(b"123456789")), case([97]), case([])]
    assert [w for _, w in res] == ["3421780262", "3904355907", "0"]
    return res


def cases():
    res = [
        case([0]),
        case([255]),
        case([0, 0, 0, 0]),
        case([255] * 4),
        case(list(b"The quick brown fox jumps over the lazy dog")),
    ]
    for n in (3, 16, 255, 4096):
        res.append(case(rand_arr(n, 0, 255)))
    res.append(case(rand_arr(2 * 10**5, 0, 255)))
    res.append(case([0] * (2 * 10**5)))
    cross_check(samples() + res)
    return [t for t, _ in res]
