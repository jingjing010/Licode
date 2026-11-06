# 固定回归向量，预期值由独立 Python 算法预先计算。
VECTORS = [('5\n', '2'), ('7\n', '0'), ('0\n', '1'), ('1\n', '0'), ('2\n', '1'), ('8\n', '7'), ('10\n', '5'), ('31\n', '0'), ('32\n', '31'), ('100\n', '27'), ('1000000000\n', '73741823'), ('999999999\n', '73741824')]

def samples():
    return VECTORS[:2]

def cases():
    return [x[0] for x in VECTORS[2:]]

def expected_cases():
    return VECTORS
