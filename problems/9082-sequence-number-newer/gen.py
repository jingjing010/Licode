# 固定回归向量，预期值由独立 Python 算法预先计算。
VECTORS = [('1\n65535\n', 'true'), ('65535\n1\n', 'false'), ('0\n0\n', 'false'), ('1\n0\n', 'true'), ('0\n1\n', 'false'), ('32768\n0\n', 'false'), ('32767\n0\n', 'true'), ('0\n32769\n', 'true'), ('65535\n65534\n', 'true'), ('100\n99\n', 'true'), ('100\n100\n', 'false'), ('0\n65535\n', 'true')]

def samples():
    return VECTORS[:2]

def cases():
    return [x[0] for x in VECTORS[2:]]

def expected_cases():
    return VECTORS
