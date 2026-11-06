# 固定回归向量，预期值由独立 Python 算法预先计算。
VECTORS = [('"a1"\n', 'false'), ('"a2"\n', 'true'), ('"a3"\n', 'false'), ('"a4"\n', 'true'), ('"a5"\n', 'false'), ('"a6"\n', 'true'), ('"a7"\n', 'false'), ('"a8"\n', 'true'), ('"b1"\n', 'true'), ('"b2"\n', 'false'), ('"b3"\n', 'true'), ('"b4"\n', 'false'), ('"b5"\n', 'true'), ('"b6"\n', 'false'), ('"b7"\n', 'true'), ('"b8"\n', 'false'), ('"c1"\n', 'false'), ('"c2"\n', 'true'), ('"c3"\n', 'false'), ('"c4"\n', 'true'), ('"c5"\n', 'false'), ('"c6"\n', 'true'), ('"c7"\n', 'false'), ('"c8"\n', 'true'), ('"d1"\n', 'true'), ('"d2"\n', 'false'), ('"d3"\n', 'true'), ('"d4"\n', 'false'), ('"d5"\n', 'true'), ('"d6"\n', 'false'), ('"d7"\n', 'true'), ('"d8"\n', 'false'), ('"e1"\n', 'false'), ('"e2"\n', 'true'), ('"e3"\n', 'false'), ('"e4"\n', 'true'), ('"e5"\n', 'false'), ('"e6"\n', 'true'), ('"e7"\n', 'false'), ('"e8"\n', 'true'), ('"f1"\n', 'true'), ('"f2"\n', 'false'), ('"f3"\n', 'true'), ('"f4"\n', 'false'), ('"f5"\n', 'true'), ('"f6"\n', 'false'), ('"f7"\n', 'true'), ('"f8"\n', 'false'), ('"g1"\n', 'false'), ('"g2"\n', 'true'), ('"g3"\n', 'false'), ('"g4"\n', 'true'), ('"g5"\n', 'false'), ('"g6"\n', 'true'), ('"g7"\n', 'false'), ('"g8"\n', 'true'), ('"h1"\n', 'true'), ('"h2"\n', 'false'), ('"h3"\n', 'true'), ('"h4"\n', 'false'), ('"h5"\n', 'true'), ('"h6"\n', 'false'), ('"h7"\n', 'true'), ('"h8"\n', 'false')]

def samples():
    return VECTORS[:2]

def cases():
    return [x[0] for x in VECTORS[2:]]

def expected_cases():
    return VECTORS
