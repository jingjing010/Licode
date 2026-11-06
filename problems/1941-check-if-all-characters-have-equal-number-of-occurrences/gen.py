# 固定回归向量，预期值由独立 Python 算法预先计算。
VECTORS = [('"abacbc"\n', 'true'), ('"aaabb"\n', 'false'), ('"a"\n', 'true'), ('"abc"\n', 'true'), ('"d"\n', 'true'), ('"ca"\n', 'true'), ('"dba"\n', 'true'), ('"bdaddde"\n', 'false'), ('"eadbbecaddabeacc"\n', 'false'), ('"aabacadbcddcabcabdcaddabadddebc"\n', 'false'), ('"beebeabdddededdccabbcedcdbecaecbddeebaecbaaaadbbbdeabeceaecccdbdcabbeacbaebcbeaaacdebeacadabddcaedad"\n', 'false'), ('"edbdeadbdaaadeecbaeeaddeadebedacbacbbdbdedbbddbdacbdbcecbeeecadddbebaabdeedbebecdaaeabadaceedcadacdedceaabdaeaecaeddcbbbbdabecbbbbdebebecdbacaecbcbbdeacacceebbbcedcdcdcbadbeaaadbcdceaddadedddebeebbebebcbdedcebecebcaeceeeecaeacccdcdceabcebaedbdbacdebeddceacabbccbbdbecbbadaeeddacceccdbaabedadbbebedacaeacdcddbadeaadbebcabcddccdcccdaeebbdaeecaacadbcbbeeececaacccbbbbddcdeeababcbdbaaaeacdddecdbbecbbacddcdcaceecacaebaddddbedcedeecccaecdbbcccacbbbeeeedeaabbcdaaaeecccdbddacdbabbbacadcdbbaeabbbcdddaebcccaeebbdceaeeddcbaaddaaadcdaacececaccaacbaedaebebebeddbaeebadecbdccddaeedbbeadadeedcdadadeebbabadedacaadebbddeeaabbcbbdcbaebecaaaebaabdceaaabbecdabeaccbaecdbbbaaadcdbeecdbaeaddbcbcaababcaadcaeaaadbacebcdedbcaedabdbbeabebeeaaddbeeacedbcebeaddbdbacaadbeebceaedcbbcaaaebeeccdaebddbdccddccaabbabcadcbbbeedebdddacaeabccebadaebdacdabacdecdddbddccdccedcccebdbdccdbaaadbbcdccbebbccceecedbdeecbcdbcdeceeaebdabaaadcbbddbcabdaeabcaddabddaedeebacbbedbcaabbdecbebeebbbaceeeacbbbeaddabdbaadebebecdeccbeadaabadaaabbdcd"\n', 'false')]

def samples():
    return VECTORS[:2]

def cases():
    return [x[0] for x in VECTORS[2:]]

def expected_cases():
    return VECTORS
