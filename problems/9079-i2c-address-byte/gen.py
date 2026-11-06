# 固定回归向量，预期值由独立 Python 算法预先计算。
VECTORS = [('0\n0\n', '0'), ('0\n1\n', '1'), ('1\n0\n', '2'), ('1\n1\n', '3'), ('39\n0\n', '78'), ('39\n1\n', '79'), ('80\n0\n', '160'), ('80\n1\n', '161'), ('104\n0\n', '208'), ('104\n1\n', '209'), ('127\n0\n', '254'), ('127\n1\n', '255')]

def samples():
    return VECTORS[:2]

def cases():
    return [x[0] for x in VECTORS[2:]]

def expected_cases():
    return VECTORS
