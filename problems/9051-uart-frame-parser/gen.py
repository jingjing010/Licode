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


def ref_parse(d):
    """下标扫描写法（与 solution.c 的逐字节状态机写法不同，用于交叉验证）"""
    out, i, n = [], 0, len(d)
    while i + 1 < n:
        if d[i] == 0xAA and d[i + 1] == 0x55:
            if i + 2 >= n:
                break
            L = d[i + 2]
            end = i + 3 + L
            if end >= n:
                break
            payload = d[i + 3:end]
            if d[end] == (L + sum(payload)) & 0xFF:
                out.append(payload)
            i = end + 1
        else:
            i += 1
    return out


def frame(payload, bad=False):
    chk = (len(payload) + sum(payload)) & 0xFF
    if bad:
        chk = (chk + random.randint(1, 255)) & 0xFF
    return [0xAA, 0x55, len(payload)] + list(payload) + [chk]


def stream(nparts, max_payload, p_good=0.6):
    """有效帧、垃圾字节、校验错误帧随机混合，最后可能跟一个截断帧"""
    d = []
    for _ in range(nparts):
        r = random.random()
        if r < p_good:
            d += frame(rand_arr(random.randint(0, max_payload), 0, 255))
        elif r < p_good + 0.15:
            d += frame(rand_arr(random.randint(0, max_payload), 0, 255), bad=True)
        elif r < p_good + 0.3:
            d += random.choice([[0xAA], [0xAA, 0xAA], [0x55], [0, 0xAA, 1]]) + rand_arr(random.randint(0, 3), 0, 255)
        else:
            d += rand_arr(random.randint(1, 5), 0, 255)
    if random.random() < 0.7:
        f = frame(rand_arr(random.randint(1, max_payload), 0, 255))
        d += f[:random.randint(1, len(f) - 1)]
    return d


def case(d):
    return lines(arr(d)), mat(ref_parse(d))


def samples():
    res = [
        case([170, 85, 2, 16, 32, 50, 0, 170, 85, 1, 7, 8]),
        case([170, 85, 1, 5, 0, 170, 85, 1, 5, 6]),
        case([170, 170, 85, 1, 3, 4, 170, 85, 3, 1, 2]),
    ]
    assert [w for _, w in res] == ["[[16,32],[7]]", "[[5]]", "[[3]]"]
    return res


def cases():
    res = [
        case([]),
        case([170, 85, 0, 0]),                       # LEN = 0 的有效帧
        case([170, 85, 0, 1]),                       # LEN = 0 但校验错
        case([170, 85]),                             # 只有帧头
        case([1, 2, 3, 170, 85, 1, 7, 8, 99]),       # 前后都有垃圾
        case([170, 85, 5, 170, 85, 0, 0]),           # 帧体里出现帧头字节，不会被重新扫描
        case(frame([0xAA, 0x55, 1, 0xAA]) + frame([9])),   # 数据中含 AA 55
        case(frame(list(range(255)))),               # LEN = 255
        case([0x55, 0xAA] * 50),
        case([170] * 100 + frame([1, 2, 3])),
        case(frame([200] * 255) + frame([200] * 255, bad=True) + frame([1])),
    ]
    for nparts, mp in ((10, 5), (50, 20), (300, 10)):
        res.append(case(stream(nparts, mp)))
    res.append(case(stream(8000, 16)))
    d = []
    while len(d) < 99990:
        d += frame(rand_arr(random.randint(0, 8), 0, 255))
    res.append(case(d[:99997]))
    res.append(case(stream(3000, 60, 0.3)[:10**5]))
    cross_check(samples() + res)
    return [t for t, _ in res]
