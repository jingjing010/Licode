# 固定回归向量，预期值由独立 Python 算法预先计算。
VECTORS = [('22\n', '2'), ('8\n', '0'), ('1\n', '0'), ('2\n', '0'), ('3\n', '1'), ('5\n', '2'), ('9\n', '3'), ('17\n', '4'), ('255\n', '1'), ('1025\n', '10'), ('1000000000\n', '3'), ('42\n', '2')]

def samples():
    return VECTORS[:2]

def cases():
    return [x[0] for x in VECTORS[2:]]

def expected_cases():
    return VECTORS
