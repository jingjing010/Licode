# 固定回归向量，预期值由独立 Python 算法预先计算。
VECTORS = [('4\n', '10'), ('10\n', '37'), ('1\n', '1'), ('2\n', '3'), ('6\n', '21'), ('7\n', '28'), ('8\n', '30'), ('14\n', '63'), ('20\n', '96'), ('28\n', '154'), ('100\n', '1060'), ('1000\n', '74926')]

def samples():
    return VECTORS[:2]

def cases():
    return [x[0] for x in VECTORS[2:]]

def expected_cases():
    return VECTORS
