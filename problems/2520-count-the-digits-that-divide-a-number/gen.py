# 固定回归向量，预期值由独立 Python 算法预先计算。
VECTORS = [('7\n', '1'), ('121\n', '2'), ('1248\n', '4'), ('1\n', '1'), ('9\n', '1'), ('11\n', '2'), ('22\n', '2'), ('123\n', '2'), ('999\n', '3'), ('11111\n', '5'), ('123456789\n', '3'), ('888888888\n', '9')]

def samples():
    return VECTORS[:2]

def cases():
    return [x[0] for x in VECTORS[2:]]

def expected_cases():
    return VECTORS
