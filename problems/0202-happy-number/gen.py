# 固定回归向量，预期值由独立 Python 算法预先计算。
VECTORS = [('19\n', 'true'), ('2\n', 'false'), ('1\n', 'true'), ('7\n', 'true'), ('10\n', 'true'), ('13\n', 'true'), ('4\n', 'false'), ('100\n', 'true'), ('111\n', 'false'), ('9999\n', 'false'), ('2147483647\n', 'false'), ('12345\n', 'false')]

def samples():
    return VECTORS[:2]

def cases():
    return [x[0] for x in VECTORS[2:]]

def expected_cases():
    return VECTORS
