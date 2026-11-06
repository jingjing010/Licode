# 固定回归向量，预期值由独立 Python 算法预先计算。
VECTORS = [('"A"\n', '1'), ('"AB"\n', '28'), ('"Z"\n', '26'), ('"AA"\n', '27'), ('"AZ"\n', '52'), ('"ZY"\n', '701'), ('"ZZ"\n', '702'), ('"AAA"\n', '703'), ('"ALL"\n', '1000'), ('"ZZZ"\n', '18278'), ('"BDWGN"\n', '1000000'), ('"FXSHRXW"\n', '2147483647')]

def samples():
    return VECTORS[:2]

def cases():
    return [x[0] for x in VECTORS[2:]]

def expected_cases():
    return VECTORS
