# 固定回归向量，预期值由独立 Python 算法预先计算。
VECTORS = [('"leEeetcode"\n', '"leetcode"'), ('"abBAcC"\n', '""'), ('"s"\n', '"s"'), ('"aA"\n', '""'), ('"B"\n', '"B"'), ('"Aa"\n', '""'), ('"bDB"\n', '"bDB"'), ('"BCdcddB"\n', '"BCdcddB"'), ('"dDdAddbAcAacBAaA"\n', '"dAddbAccBA"'), ('"ddBDABaACaCCadDdcbbddBdDDbBccAd"\n', '"ddBDABCaCCadcbbddBDccAd"'), ('"bDcdABdABbbDcbbCDbCDCAbCAaAAcBaaDaaddaacbDBCcaCDBbcCCACCadddbdDccbcaaAaaBAdcAccbDacdbBadBBcadadAbBab"\n', '"bDcdABdAbDcbbCDbCDCAbCAAcBaaDaaddaacbDBaCDCACCadddbccbcaaaBAdcAccbDacdadBBcadadb"')]

def samples():
    return VECTORS[:2]

def cases():
    return [x[0] for x in VECTORS[2:]]

def expected_cases():
    return VECTORS
