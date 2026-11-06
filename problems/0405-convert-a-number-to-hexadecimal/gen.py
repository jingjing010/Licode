# 固定回归向量，预期值由独立 Python 算法预先计算。
VECTORS = [('26\n', '"1a"'), ('-1\n', '"ffffffff"'), ('0\n', '"0"'), ('1\n', '"1"'), ('16\n', '"10"'), ('255\n', '"ff"'), ('256\n', '"100"'), ('-2147483648\n', '"80000000"'), ('2147483647\n', '"7fffffff"'), ('-16\n', '"fffffff0"'), ('4096\n', '"1000"'), ('123456\n', '"1e240"')]

def samples():
    return VECTORS[:2]

def cases():
    return [x[0] for x in VECTORS[2:]]

def expected_cases():
    return VECTORS
