# 固定回归向量，预期值由独立 Python 算法预先计算。
VECTORS = [('10\n0\n1000\n', '10'), ('10\n4\n1000\n', '160'), ('10\n10\n1000\n', '1000'), ('1\n31\n2147483647\n', '2147483647'), ('0\n100\n100\n', '0'), ('100\n5\n50\n', '50'), ('3\n3\n23\n', '23'), ('3\n3\n24\n', '24'), ('3\n3\n25\n', '24'), ('1\n1\n1\n', '1'), ('5\n2\n100\n', '20'), ('1\n100\n1000000\n', '1000000')]

def samples():
    return VECTORS[:2]

def cases():
    return [x[0] for x in VECTORS[2:]]

def expected_cases():
    return VECTORS
