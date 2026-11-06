# 固定回归向量，预期值由独立 Python 算法预先计算。
VECTORS = [('"USA"\n', 'true'), ('"FlaG"\n', 'false'), ('"Google"\n', 'true'), ('"leetcode"\n', 'true'), ('"a"\n', 'true'), ('"aB"\n', 'false'), ('"BbB"\n', 'false'), ('"BBbbBBb"\n', 'false'), ('"zBaAAzbaBbbBBbZa"\n', 'false'), ('"ZZAzbBbZBBZzZZZAZZZaaABBbbzbZzZ"\n', 'false'), ('"ZZazbaAzbZbZBzZazbabbzzabABzAABbbzAAbBZZBzBAaABAzAbAABBaBbAzZZbzabBZBABaazBzZZZAzaBBbaZBBbAabAaAAaAZ"\n', 'false')]

def samples():
    return VECTORS[:2]

def cases():
    return [x[0] for x in VECTORS[2:]]

def expected_cases():
    return VECTORS
