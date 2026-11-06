# 固定回归向量，预期值由独立 Python 算法预先计算。
VECTORS = [('5\n', 'true'), ('3\n', 'false'), ('0\n', 'true'), ('1\n', 'true'), ('2\n', 'true'), ('4\n', 'true'), ('7\n', 'false'), ('25\n', 'true'), ('65\n', 'true'), ('9999\n', 'false'), ('2147483647\n', 'false'), ('2147395600\n', 'true')]

def samples():
    return VECTORS[:2]

def cases():
    return [x[0] for x in VECTORS[2:]]

def expected_cases():
    return VECTORS
