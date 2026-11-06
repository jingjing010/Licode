# 固定回归向量，预期值由独立 Python 算法预先计算。
VECTORS = [('"aba"\n', 'true'), ('"abca"\n', 'true'), ('"abc"\n', 'false'), ('"a"\n', 'true'), ('"e"\n', 'true'), ('"de"\n', 'true'), ('"bee"\n', 'true'), ('"ccdecdb"\n', 'false'), ('"ddeeecbcceedecba"\n', 'false'), ('"eacdeeeabecbbdcdaeadcacccabeddd"\n', 'false'), ('"cddabdeedadadddaabdcddecccaddaadbcdaaccabbbdcdecbccbdeeeedceddbbbbdbaebdbbdaeeacebdecbdadccbdbbbccdd"\n', 'false'), ('"ddbececedcbbabddeeecaabdcaabbcadbeddbecccabddbbbbbbecacdadcacccbeceabbedbebdaacbeadedcababadccdeceaacabbdaadbeaaceeabdedacbedcecabdcbdadbbecedacdccecdbeddebedabacedbbbecbaccecdaadcedbbaadacdeddcbbdecccbbdbddeceabeaccededdeebabadbaeabbccbaadeaadeaabcedeabcbeceecbdabeaaceaceeccbcdecaebabbeabcaebbbbaadebbaebccadceebdeadecbacccededdebcccccdcacdacacaabbdbedecededabcebabbabebcbbccebeddcaddeccbbdbcadecabecadcbdaeddaedaccccbbcdacccbcebeacdcdedaaeaceadcbcdacbdbedaadcdcadbadeacebdabbebeecaebaeacccadddacbdcccebedbbecdaadeedaeaabadbaaaccbceaedbbbbaddeeadccceacebcbbaacaceccbeddddcdecadcadcccceabcdceaebdabeeedebdcadcacbcbdcacabcdaedaecbdaaeabaedeebaadcedaaecdccdedadaccdedcbecddbdedecdeaaceadaaedaaccececadcccadabaedadaaabaeeacbccdbaeeaabeeddedaeccdcbbecdaaabedcabcbdedbcececebdbdaeebbbceddcebdccabaadbecadadbdeedebdcecdeecdacaadeddbcaacceeeeaebaeabaaceceebabdadebdcacedcdeccdebaacddecedacbeebeaaacaeaaaabdaaacbbbeaecaccaebeaaaddcacacccecbedebeceaccbaabdeddcceecedadebaabdeddbebedebbaceabdbaaddbbcaaeeddbbd"\n', 'false')]

def samples():
    return VECTORS[:2]

def cases():
    return [x[0] for x in VECTORS[2:]]

def expected_cases():
    return VECTORS
