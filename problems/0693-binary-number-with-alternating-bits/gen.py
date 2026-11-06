# 固定回归向量，预期值由独立 Python 算法预先计算。
VECTORS = [('5\n', 'true'), ('7\n', 'false'), ('1\n', 'true'), ('2\n', 'true'), ('3\n', 'false'), ('10\n', 'true'), ('11\n', 'false'), ('21\n', 'true'), ('42\n', 'true'), ('85\n', 'true'), ('1431655765\n', 'true'), ('2147483647\n', 'false')]

def samples():
    return VECTORS[:2]

def cases():
    return [x[0] for x in VECTORS[2:]]

def expected_cases():
    return VECTORS
