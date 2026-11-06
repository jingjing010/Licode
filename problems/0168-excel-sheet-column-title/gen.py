# 固定回归向量，预期值由独立 Python 算法预先计算。
VECTORS = [('1\n', '"A"'), ('28\n', '"AB"'), ('26\n', '"Z"'), ('27\n', '"AA"'), ('52\n', '"AZ"'), ('701\n', '"ZY"'), ('702\n', '"ZZ"'), ('703\n', '"AAA"'), ('1000\n', '"ALL"'), ('18278\n', '"ZZZ"'), ('2147483647\n', '"FXSHRXW"'), ('1000000\n', '"BDWGN"')]

def samples():
    return VECTORS[:2]

def cases():
    return [x[0] for x in VECTORS[2:]]

def expected_cases():
    return VECTORS
