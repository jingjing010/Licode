# 固定回归向量，预期值由独立 Python 算法预先计算。
VECTORS = [('"Hello"\n', '"hello"'), ('"LOVELY"\n', '"lovely"'), ('"al&phaBET"\n', '"al&phabet"'), ('"here"\n', '"here"'), ('"?"\n', '"?"'), ('"0a"\n', '"0a"'), ('"BAb"\n', '"bab"'), ('"A!9aa9?"\n', '"a!9aa9?"'), ('"?B1A0A?1Aa9!?A0B"\n', '"?b1a0a?1aa9!?a0b"'), ('"A1bb?AAaB0b0?B0aA!??1Ba!a1?ab!0"\n', '"a1bb?aaab0b0?b0aa!??1ba!a1?ab!0"'), ('"9!0b0!!bABa!b1b0A!bb?A0BabA?abb00?9BB1B!00!9A0?9!09bBaBB1A1190B19BB1a?100ba99B?991AB?bB!1Bab09!A0B09"\n', '"9!0b0!!baba!b1b0a!bb?a0baba?abb00?9bb1b!00!9a0?9!09bbabb1a1190b19bb1a?100ba99b?991ab?bb!1bab09!a0b09"')]

def samples():
    return VECTORS[:2]

def cases():
    return [x[0] for x in VECTORS[2:]]

def expected_cases():
    return VECTORS
