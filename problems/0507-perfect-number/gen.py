# 固定回归向量，预期值由独立 Python 算法预先计算。
VECTORS = [('28\n', 'true'), ('7\n', 'false'), ('1\n', 'false'), ('2\n', 'false'), ('6\n', 'true'), ('12\n', 'false'), ('16\n', 'false'), ('496\n', 'true'), ('8128\n', 'true'), ('33550336\n', 'true'), ('99999999\n', 'false'), ('100000000\n', 'false')]

def samples():
    return VECTORS[:2]

def cases():
    return [x[0] for x in VECTORS[2:]]

def expected_cases():
    return VECTORS
