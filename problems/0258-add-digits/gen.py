# 固定回归向量，预期值由独立 Python 算法预先计算。
VECTORS = [('38\n', '2'), ('0\n', '0'), ('1\n', '1'), ('9\n', '9'), ('10\n', '1'), ('99\n', '9'), ('123\n', '6'), ('99999\n', '9'), ('1000000\n', '1'), ('2147483647\n', '1'), ('18\n', '9'), ('19\n', '1')]

def samples():
    return VECTORS[:2]

def cases():
    return [x[0] for x in VECTORS[2:]]

def expected_cases():
    return VECTORS
