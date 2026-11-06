# 固定回归向量，预期值由独立 Python 算法预先计算。
VECTORS = [('0\n0\n', 'true'), ('0\n1\n', 'false'), ('1\n0\n', 'false'), ('1\n1\n', 'true'), ('3\n0\n', 'true'), ('3\n1\n', 'false'), ('7\n0\n', 'false'), ('7\n1\n', 'true'), ('128\n0\n', 'false'), ('128\n1\n', 'true'), ('255\n0\n', 'true'), ('255\n1\n', 'false')]

def samples():
    return VECTORS[:2]

def cases():
    return [x[0] for x in VECTORS[2:]]

def expected_cases():
    return VECTORS
