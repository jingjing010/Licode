# 固定回归向量，预期值由独立 Python 算法预先计算。
VECTORS = [('250\n20\n256\n', '2'), ('256\n256\n256\n', '1'), ('0\n0\n256\n', '0'), ('0\n1\n256\n', '1'), ('255\n1\n256\n', '1'), ('255\n2\n256\n', '2'), ('1\n256\n256\n', '2'), ('0\n512\n256\n', '2'), ('1023\n1025\n1024\n', '2'), ('4294967295\n1\n256\n', '1'), ('100\n100000\n4096\n', '25'), ('0\n1\n1\n', '1')]

def samples():
    return VECTORS[:2]

def cases():
    return [x[0] for x in VECTORS[2:]]

def expected_cases():
    return VECTORS
