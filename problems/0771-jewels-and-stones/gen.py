# 固定回归向量，预期值由独立 Python 算法预先计算。
VECTORS = [('"aA"\n"aAAbbbb"\n', '3'), ('"z"\n"ZZ"\n', '0'), ('"a"\n"a"\n', '1'), ('"a"\n"aAABbb"\n', '1'), ('"a"\n"xyz"\n', '0'), ('"a"\n"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"\n', '50'), ('"AB"\n"a"\n', '0'), ('"AB"\n"aAABbb"\n', '3'), ('"AB"\n"xyz"\n', '0'), ('"AB"\n"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"\n', '0'), ('"aBc"\n"a"\n', '1'), ('"aBc"\n"aAABbb"\n', '2'), ('"aBc"\n"xyz"\n', '0'), ('"aBc"\n"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"\n', '50')]

def samples():
    return VECTORS[:2]

def cases():
    return [x[0] for x in VECTORS[2:]]

def expected_cases():
    return VECTORS
