# 固定回归向量，预期值由独立 Python 算法预先计算。
VECTORS = [('3\n', '1'), ('0\n', '0'), ('1\n', '1'), ('2\n', '1'), ('4\n', '2'), ('9\n', '3'), ('15\n', '3'), ('16\n', '4'), ('9999\n', '99'), ('10000\n', '100'), ('1000000000\n', '31622'), ('999999999\n', '31622')]

def samples():
    return VECTORS[:2]

def cases():
    return [x[0] for x in VECTORS[2:]]

def expected_cases():
    return VECTORS
