# 固定回归向量，预期值由独立 Python 算法预先计算。
VECTORS = [('196\n8\n', '3'), ('4294967295\n32\n', '0'), ('0\n32\n', '32'), ('0\n0\n', '0'), ('1\n1\n', '0'), ('0\n1\n', '1'), ('2863311530\n32\n', '1'), ('4294901760\n32\n', '16'), ('4294901760\n16\n', '16'), ('2147483648\n32\n', '31'), ('1\n32\n', '31'), ('16711680\n24\n', '16')]

def samples():
    return VECTORS[:2]

def cases():
    return [x[0] for x in VECTORS[2:]]

def expected_cases():
    return VECTORS
