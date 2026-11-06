import os

from genlib import *

PID = 9051


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


def ref(d):
    """按下标扫描的写法（与 C 里的逐字节状态机写法不同，用来交叉验证）"""
    out, i, n = [], 0, len(d)
    while i < n:
        if d[i] != 0xAA:
            i += 1
            continue
        j = i + 1
        while j < n and d[j] == 0xAA:      # 连续的 AA，最后一个才是帧头 1
            j += 1
        if j >= n:
            break
        if d[j] != 0x55:
            i = j + 1
            continue
        if j + 1 >= n:
            break
        L = d[j + 1]
        end = j + 2 + L                    # 校验字节的下标
        if end >= n:
            break
        payload = d[j + 2:end]
        if (L + sum(payload)) & 0xFF == d[end]:
            out.append(payload)
        i = end + 1
    return out


def frame(payload):
    return [0xAA, 0x55, len(payload)] + list(payload) + [(len(payload) + sum(payload)) & 0xFF]


def case(d):
    d = list(d)
    return lines(arr(d)), mat(ref(d))


def stream(nparts, max_payload):
    """有效帧、垃圾字节、校验错误帧、连续 AA 随机混合"""
    d = []
    for _ in range(nparts):
        r = random.random()
        if r < 0.5:
            d += frame(rand_arr(random.randint(0, max_payload), 0, 255))
        elif r < 0.65:
            d += rand_arr(random.randint(1, 5), 0, 255)
        elif r < 0.8:
            f = frame(rand_arr(random.randint(0, max_payload), 0, 255))
            f[-1] = (f[-1] + random.randint(1, 255)) & 0xFF
            d += f
        elif r < 0.9:
            d += [0xAA] * random.randint(1, 3)
        else:
            d += [0xAA, 0x55, 0xAA, 0x55][:random.randint(1, 4)]
    return d


SAMPLES = [
    ([170, 85, 2, 16, 32, 50, 0, 170, 85, 1, 7, 8], "[[16,32],[7]]"),
    ([170, 85, 1, 5, 0, 170, 85, 1, 5, 6], "[[5]]"),
    ([170, 170, 85, 1, 3, 4, 170, 85, 3, 1, 2], "[[3]]"),
]


def samples():
    res = []
    for d, want in SAMPLES:
        text, got = case(d)
        assert got == want
        res.append((text, want))
    return res


def cases():
    res = [
        case([]),
        case([0xAA]),
        case([0xAA, 0x55]),
        case([0xAA, 0x55, 0, 0]),              # LEN = 0 的有效帧
        case([0xAA, 0x55, 0, 1]),              # LEN = 0，校验错
        case([0xAA, 0x55, 1, 7]),              # 缺校验字节
        case([0, 0, 99] + frame([0xAA, 0x55, 9]) + [1, 2, 3]),   # 数据里含 AA 55
        case([0xAA, 0x55, 5, 0xAA, 0x55, 0, 0]),  # 帧不完整：后面的 AA 55 只会被当作数据
        case(frame([]) + frame([255] * 50) + frame([1, 2, 3])),
        case(frame(list(range(256))[:255])),  # 最长帧，和溢出
        case(frame([0x55] * 9)[:-1] + [0]),
        case([0xAA] * 10 + [0x55, 1, 4, 5]),
    ]
    for parts, mp in ((10, 5), (50, 10), (300, 20)):
        res.append(case(stream(parts, mp)))
    s = stream(8000, 30)
    res.append(case(s[:10**5]))
    res.append(case(rand_arr(10**5, 0, 255)))     # 纯噪声
    d = []
    while len(d) < 99997:
        d += frame(rand_arr(random.randint(0, 3), 0, 255))
    res.append(case(d[:10**5]))
    cross_check(samples() + res)
    return [t for t, _ in res]
