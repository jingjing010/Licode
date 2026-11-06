# 固定回归向量，预期值由独立 Python 算法预先计算。
VECTORS = [('0\n10\n20\n', 'false'), ('1\n10\n20\n', 'false'), ('9\n10\n20\n', 'false'), ('10\n10\n20\n', 'true'), ('11\n10\n20\n', 'true'), ('15\n10\n20\n', 'true'), ('19\n10\n20\n', 'true'), ('20\n10\n20\n', 'true'), ('21\n10\n20\n', 'false'), ('100\n10\n20\n', 'false'), ('2147483648\n10\n20\n', 'false'), ('4294967295\n10\n20\n', 'false')]

def samples():
    return VECTORS[:2]

def cases():
    return [x[0] for x in VECTORS[2:]]

def expected_cases():
    return VECTORS
