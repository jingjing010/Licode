# 固定回归向量，预期值由独立 Python 算法预先计算。
VECTORS = [('2\n', 'true'), ('3\n', 'false'), ('1\n', 'false'), ('4\n', 'true'), ('5\n', 'false'), ('6\n', 'true'), ('7\n', 'false'), ('10\n', 'true'), ('99\n', 'false'), ('100\n', 'true'), ('999\n', 'false'), ('1000\n', 'true')]

def samples():
    return VECTORS[:2]

def cases():
    return [x[0] for x in VECTORS[2:]]

def expected_cases():
    return VECTORS
