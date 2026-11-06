# 固定回归向量，预期值由独立 Python 算法预先计算。
VECTORS = [('"a1c1e1"\n', '"abcdef"'), ('"a1b2c3d4e"\n', '"abbdcfdhe"'), ('"a"\n', '"a"'), ('"z0"\n', '"zz"'), ('"a9"\n', '"aj"'), ('"q9"\n', '"qz"'), ('"a0a0"\n', '"aaaa"'), ('"b2c3"\n', '"bdcf"'), ('"x2"\n', '"xz"'), ('"a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1"\n', '"abababababababababababababababababababababababababababababababababababababababababababababababababab"'), ('"m3m3m3m3m3m3m3m3m3m3m3m3m3m3m3m3m3m3m3m3m3m3m3m3m3m3m3m3m3m3m3m3m3m3m3m3m3m3m3m3z"\n', '"mpmpmpmpmpmpmpmpmpmpmpmpmpmpmpmpmpmpmpmpmpmpmpmpmpmpmpmpmpmpmpmpmpmpmpmpmpmpmpmpz"'), ('"q9q0"\n', '"qzqq"')]

def samples():
    return VECTORS[:2]

def cases():
    return [x[0] for x in VECTORS[2:]]

def expected_cases():
    return VECTORS
