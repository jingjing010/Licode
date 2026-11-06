# 固定回归向量，预期值由独立 Python 算法预先计算。
VECTORS = [('100\n100\n', 'true'), ('99\n100\n', 'false'), ('101\n100\n', 'true'), ('2\n4294967295\n', 'true'), ('4294967295\n2\n', 'false'), ('0\n0\n', 'true'), ('0\n1\n', 'false'), ('1\n0\n', 'true'), ('2147483647\n0\n', 'true'), ('0\n2147483647\n', 'false'), ('4294967294\n4294967295\n', 'false'), ('10\n5\n', 'true')]

def samples():
    return VECTORS[:2]

def cases():
    return [x[0] for x in VECTORS[2:]]

def expected_cases():
    return VECTORS
