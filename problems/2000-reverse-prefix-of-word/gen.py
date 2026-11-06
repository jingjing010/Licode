# 固定回归向量，预期值由独立 Python 算法预先计算。
VECTORS = [('"abcdefd"\n100\n', '"dcbaefd"'), ('"xyxzxe"\n122\n', '"zxyxxe"'), ('"a"\n97\n', '"a"'), ('"a"\n99\n', '"a"'), ('"a"\n122\n', '"a"'), ('"abcabc"\n97\n', '"abcabc"'), ('"abcabc"\n99\n', '"cbaabc"'), ('"abcabc"\n122\n', '"abcabc"'), ('"abcd"\n97\n', '"abcd"'), ('"abcd"\n99\n', '"cbad"'), ('"abcd"\n122\n', '"abcd"')]

def samples():
    return VECTORS[:2]

def cases():
    return [x[0] for x in VECTORS[2:]]

def expected_cases():
    return VECTORS
