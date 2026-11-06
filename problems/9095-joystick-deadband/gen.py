# 固定回归向量，预期值由独立 Python 算法预先计算。
VECTORS = [('10\n5\n', '5'), ('-10\n5\n', '-5'), ('5\n5\n', '0'), ('-5\n5\n', '0'), ('0\n5\n', '0'), ('1\n0\n', '1'), ('-1\n0\n', '-1'), ('32767\n100\n', '32667'), ('-32768\n100\n', '-32668'), ('100\n200\n', '0'), ('-100\n200\n', '0'), ('0\n0\n', '0')]

def samples():
    return VECTORS[:2]

def cases():
    return [x[0] for x in VECTORS[2:]]

def expected_cases():
    return VECTORS
