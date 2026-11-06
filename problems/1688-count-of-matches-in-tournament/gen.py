# 固定回归向量，预期值由独立 Python 算法预先计算。
VECTORS = [('7\n', '6'), ('14\n', '13'), ('1\n', '0'), ('2\n', '1'), ('3\n', '2'), ('4\n', '3'), ('5\n', '4'), ('8\n', '7'), ('16\n', '15'), ('63\n', '62'), ('100\n', '99'), ('200\n', '199')]

def samples():
    return VECTORS[:2]

def cases():
    return [x[0] for x in VECTORS[2:]]

def expected_cases():
    return VECTORS
