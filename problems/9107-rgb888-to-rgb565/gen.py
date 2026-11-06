# 固定回归向量，预期值由独立 Python 算法预先计算。
VECTORS = [('255\n0\n0\n', '63488'), ('0\n255\n0\n', '2016'), ('0\n0\n255\n', '31'), ('255\n255\n255\n', '65535'), ('0\n0\n0\n', '0'), ('128\n128\n128\n', '33808'), ('7\n3\n7\n', '0'), ('8\n4\n8\n', '2081'), ('1\n2\n3\n', '0'), ('31\n63\n31\n', '6627'), ('100\n150\n200\n', '25785'), ('254\n254\n254\n', '65535')]

def samples():
    return VECTORS[:2]

def cases():
    return [x[0] for x in VECTORS[2:]]

def expected_cases():
    return VECTORS
