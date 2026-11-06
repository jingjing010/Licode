# 固定回归向量，预期值由独立 Python 算法预先计算。
VECTORS = [('4\n', '4'), ('25\n', '1389537'), ('0\n', '0'), ('1\n', '1'), ('2\n', '1'), ('3\n', '2'), ('5\n', '7'), ('10\n', '149'), ('15\n', '3136'), ('20\n', '66012'), ('30\n', '29249425'), ('37\n', '2082876103')]

def samples():
    return VECTORS[:2]

def cases():
    return [x[0] for x in VECTORS[2:]]

def expected_cases():
    return VECTORS
