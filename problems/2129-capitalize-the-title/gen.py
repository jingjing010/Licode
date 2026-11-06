# 固定回归向量，预期值由独立 Python 算法预先计算。
VECTORS = [('"capiTalIze tHe titLe"\n', '"Capitalize The Title"'), ('"First leTTeR of EACH Word"\n', '"First Letter of Each Word"'), ('"b"\n', '"b"'), ('"Ac"\n', '"ac"'), ('"CBc"\n', '"Cbc"'), ('"bCaaBCA"\n', '"Bcaabca"'), ('"bBbaaaaCCbCacccc"\n', '"Bbbaaaaccbcacccc"'), ('"cbacBCCCaAbbbbbAabBbBAcCACBABaB"\n', '"Cbacbcccaabbbbbaabbbbaccacbabab"'), ('"CAcCCAAcbBAcBAccbbbabccCaCcbbABbCacaBBaCCbaCcABCbBcbbcbBbaaAaBcCCAAcaABaaCBbBbcacaBCBCAaCccbBAaccBAA"\n', '"Cacccaacbbacbaccbbbabcccaccbbabbcacabbaccbaccabcbbcbbcbbbaaaabcccaacaabaacbbbbcacabcbcaacccbbaaccbaa"'), ('"BAAbaaB"\n', '"Baabaab"'), ('"baaaabaA"\n', '"Baaaabaa"'), ('"AAAbaAaBbb"\n', '"Aaabaaabbb"')]

def samples():
    return VECTORS[:2]

def cases():
    return [x[0] for x in VECTORS[2:]]

def expected_cases():
    return VECTORS
