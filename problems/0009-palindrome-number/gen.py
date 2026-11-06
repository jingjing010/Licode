# 固定回归向量，预期值由独立 Python 算法预先计算。
VECTORS = [('121\n', 'true'), ('-121\n', 'false'), ('0\n', 'true'), ('10\n', 'false'), ('1\n', 'true'), ('11\n', 'true'), ('1001\n', 'true'), ('12321\n', 'true'), ('123\n', 'false'), ('2147483647\n', 'false'), ('1000000001\n', 'true'), ('1221\n', 'true')]

def samples():
    return VECTORS[:2]

def cases():
    return [x[0] for x in VECTORS[2:]]

def expected_cases():
    return VECTORS
