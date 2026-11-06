from genlib import *


def ref(buf):
    return (-sum(buf)) % 256


def ref2(buf):
    # 按定义暴力枚举校验和，与 ref 交叉验证
    for c in range(256):
        if (sum(buf) + c) % 256 == 0:
            return c


def parse(line):
    line = line.strip()[1:-1]
    return [int(t) for t in line.split(",")] if line else []


def expected(text):
    return str(ref(parse(text.split("\n")[0])))


def hex_record(rec):
    # ":0300300002337A1E" -> 数据字节（不含末尾校验和）及校验和
    bs = bytes.fromhex(rec[1:])
    return list(bs[:-1]), bs[-1]


def samples():
    res = [
        (lines(arr([3, 0, 48, 0, 2, 51, 122])), "30"),
        (lines(arr([255, 1])), "0"),
        (lines(arr([200, 100, 50])), "162"),
    ]
    for inp, out in res:
        assert expected(inp) == out
    return res


def cases():
    data = [
        [],
        [0],
        [1],
        [255],
        [128, 128],
        [0, 0, 0, 0],
        [255] * 100,
        [1] * 256,
    ]
    # 真实的 Intel HEX 记录，校验和是已知的
    for rec in (":10010000214601360121470136007EFE09D2190140",
                ":100110002146017E17C20001FF5F16002148011928",
                ":00000001FF",
                ":020000040800F2"):
        buf, c = hex_record(rec)
        assert ref(buf) == c
        data.append(buf)
    data.append(rand_arr(20, 0, 255))
    data.append(rand_arr(1000, 0, 255))
    data.append(rand_arr(10000, 0, 255))
    data.append(rand_arr(10000, 250, 255))
    for buf in data:
        assert 0 <= len(buf) <= 10000 and all(0 <= v <= 255 for v in buf)
        assert ref(buf) == ref2(buf)
    return [lines(arr(buf)) for buf in data]
