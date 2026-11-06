# 固定回归向量，预期值由独立 Python 算法预先计算。
VECTORS = [('4\n', 'false'), ('1\n', 'true'), ('2\n', 'true'), ('3\n', 'true'), ('5\n', 'true'), ('8\n', 'false'), ('9\n', 'true'), ('12\n', 'false'), ('100\n', 'false'), ('101\n', 'true'), ('2147483647\n', 'true'), ('2147483644\n', 'false')]

def samples():
    return VECTORS[:2]

def cases():
    return [x[0] for x in VECTORS[2:]]

def expected_cases():
    return VECTORS
