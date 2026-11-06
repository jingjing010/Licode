# 固定回归向量，预期值由独立 Python 算法预先计算。
VECTORS = [('6\n', 'true'), ('14\n', 'false'), ('1\n', 'true'), ('0\n', 'false'), ('-6\n', 'false'), ('2\n', 'true'), ('3\n', 'true'), ('5\n', 'true'), ('30\n', 'true'), ('49\n', 'false'), ('2147483647\n', 'false'), ('536870912\n', 'true')]

def samples():
    return VECTORS[:2]

def cases():
    return [x[0] for x in VECTORS[2:]]

def expected_cases():
    return VECTORS
