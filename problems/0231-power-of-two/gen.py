# 固定回归向量，预期值由独立 Python 算法预先计算。
VECTORS = [('1\n', 'true'), ('3\n', 'false'), ('0\n', 'false'), ('-1\n', 'false'), ('2\n', 'true'), ('4\n', 'true'), ('8\n', 'true'), ('16\n', 'true'), ('1023\n', 'false'), ('1024\n', 'true'), ('1073741824\n', 'true'), ('2147483647\n', 'false')]

def samples():
    return VECTORS[:2]

def cases():
    return [x[0] for x in VECTORS[2:]]

def expected_cases():
    return VECTORS
