# 固定回归向量，预期值由独立 Python 算法预先计算。
VECTORS = [('"bank"\n"kanb"\n', 'true'), ('"attack"\n"defend"\n', 'false'), ('"a"\n"a"\n', 'true'), ('"a"\n"b"\n', 'false'), ('"ab"\n"ba"\n', 'true'), ('"ab"\n"aa"\n', 'false'), ('"abc"\n"cba"\n', 'true'), ('"abc"\n"bca"\n', 'false'), ('"aaaa"\n"aaaa"\n', 'true'), ('"abcd"\n"abdc"\n', 'true'), ('"aabb"\n"bbaa"\n', 'false'), ('"abc"\n"abd"\n', 'false')]

def samples():
    return VECTORS[:2]

def cases():
    return [x[0] for x in VECTORS[2:]]

def expected_cases():
    return VECTORS
