# 固定回归向量，预期值由独立 Python 算法预先计算。
VECTORS = [('2\n', '3'), ('3\n', '2'), ('1\n', '1'), ('-1\n', '1'), ('-2\n', '3'), ('4\n', '3'), ('5\n', '5'), ('6\n', '3'), ('7\n', '5'), ('1000000000\n', '44723'), ('-1000000000\n', '44723'), ('999\n', '45')]

def samples():
    return VECTORS[:2]

def cases():
    return [x[0] for x in VECTORS[2:]]

def expected_cases():
    return VECTORS
