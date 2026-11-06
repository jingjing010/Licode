# 固定回归向量，预期值由独立 Python 算法预先计算。
VECTORS = [('"Hello, my name is John"\n', '5'), ('"Hello"\n', '1'), ('""\n', '0'), ('"   "\n', '0'), ('"c"\n', '1'), ('"a "\n', '1'), ('"b  "\n', '1'), ('"!cab , "\n', '2'), ('"cbc a!!acaa,bab "\n', '2'), ('"! ,!a! ,ccac, a c,b ,ac, ,c!, !"\n', '8'), ('",!! b  ,a ac cb a,,,,!!   , ! cbc,b   bb, ,,! !a a ! , !,a,a  bb babb ab,a! aa! ,b , ab! , aabcb c,c"\n', '26')]

def samples():
    return VECTORS[:2]

def cases():
    return [x[0] for x in VECTORS[2:]]

def expected_cases():
    return VECTORS
