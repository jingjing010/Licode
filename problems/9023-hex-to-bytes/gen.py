from genlib import *
import json

HEX = "0123456789abcdefABCDEF"


def ref(h):
    if len(h) % 2 or any(c not in HEX for c in h):
        return -1, None
    return len(h) // 2, list(bytes.fromhex(h))


def expected(text):
    r, data = ref(json.loads(text.split("\n")[0]))
    return str(r) if r < 0 else "%d\n%s" % (r, arr(data))


def samples():
    res = [
        (lines(s("1234abCD")), "4\n[18,52,171,205]"),
        (lines(s("00ff0A")), "3\n[0,255,10]"),
        (lines(s("12G4")), "-1"),
    ]
    for inp, out in res:
        assert expected(inp) == out
    return res


def cases():
    data = [
        "",
        "00",
        "FF",
        "7f80",
        "123",
        "1",
        "0123456789abcdefABCDEF",
        "12 34",
        "0x12",
        "aG",
        "AT+KEY",
        "00112233445566778899aabbccddeeff",
        rand_str(200, HEX),
        rand_str(2000, HEX),
        rand_str(999, HEX),
        rand_str(1000, HEX) + "z" + rand_str(999, HEX),
        "/:@`gG",
    ]
    for h in data:
        assert len(h) <= 2000
        r, b = ref(h)
        if r >= 0:
            assert "".join("%02x" % x for x in b) == h.lower()
    return [lines(s(h)) for h in data]
