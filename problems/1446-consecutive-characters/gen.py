# 固定回归向量，预期值由独立 Python 算法预先计算。
VECTORS = [('"leetcode"\n', '2'), ('"abbcccddddeeeeedcba"\n', '5'), ('"a"\n', '1'), ('"aaaa"\n', '4'), ('"c"\n', '1'), ('"ae"\n', '1'), ('"bad"\n', '1'), ('"ebdacad"\n', '1'), ('"ecdabececababeea"\n', '2'), ('"debebcaebcaedcdebbbddadcabdbbbb"\n', '4'), ('"daaacdabaabddedaabcbdcbedcdecedbbdedcebddeccadaddbadcbddeeabaeabcbdcbaaaaecdbaccbddbebccbdadaccadeec"\n', '4')]

def samples():
    return VECTORS[:2]

def cases():
    return [x[0] for x in VECTORS[2:]]

def expected_cases():
    return VECTORS
