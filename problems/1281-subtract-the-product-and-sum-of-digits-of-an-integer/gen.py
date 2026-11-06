# 固定回归向量，预期值由独立 Python 算法预先计算。
VECTORS = [('234\n', '15'), ('4421\n', '21'), ('1\n', '0'), ('9\n', '0'), ('10\n', '-1'), ('100\n', '-1'), ('101\n', '-2'), ('999\n', '702'), ('123456\n', '699'), ('100000\n', '-1'), ('99999\n', '59004'), ('25\n', '3')]

def samples():
    return VECTORS[:2]

def cases():
    return [x[0] for x in VECTORS[2:]]

def expected_cases():
    return VECTORS
