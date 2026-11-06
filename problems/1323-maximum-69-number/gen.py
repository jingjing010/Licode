# 固定回归向量，预期值由独立 Python 算法预先计算。
VECTORS = [('9669\n', '9969'), ('9996\n', '9999'), ('6\n', '9'), ('9\n', '9'), ('66\n', '96'), ('69\n', '99'), ('96\n', '99'), ('99\n', '99'), ('666\n', '966'), ('696\n', '996'), ('999\n', '999'), ('6666\n', '9666')]

def samples():
    return VECTORS[:2]

def cases():
    return [x[0] for x in VECTORS[2:]]

def expected_cases():
    return VECTORS
