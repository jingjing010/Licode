# 固定回归向量，预期值由独立 Python 算法预先计算。
VECTORS = [('"abcde"\n"cdeab"\n', 'true'), ('"abcde"\n"abced"\n', 'false'), ('"a"\n"a"\n', 'true'), ('"ab"\n"a"\n', 'false'), ('"abc"\n"abc"\n', 'true'), ('"abc"\n"bca"\n', 'true'), ('"abc"\n"cab"\n', 'true'), ('"aaaa"\n"aaaa"\n', 'true'), ('"aaaa"\n"aaaa"\n', 'true'), ('"aaaa"\n"aaaa"\n', 'true'), ('"abacaba"\n"abacaba"\n', 'true'), ('"abacaba"\n"bacabaa"\n', 'true'), ('"abacaba"\n"acabaab"\n', 'true')]

def samples():
    return VECTORS[:2]

def cases():
    return [x[0] for x in VECTORS[2:]]

def expected_cases():
    return VECTORS
