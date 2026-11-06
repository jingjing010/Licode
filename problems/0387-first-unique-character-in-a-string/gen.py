# 固定回归向量，预期值由独立 Python 算法预先计算。
VECTORS = [('"leetcode"\n', '0'), ('"loveleetcode"\n', '2'), ('"aabb"\n', '-1'), ('"z"\n', '0'), ('"d"\n', '0'), ('"ba"\n', '0'), ('"bbb"\n', '-1'), ('"cceaeba"\n', '5'), ('"abedcabeebdeadba"\n', '4'), ('"beeaaebebbaabaeeccceedcaaaacbba"\n', '21'), ('"edaabcddcddaaddeacdcaeeccebdecadabcaaaceeaccddbbdedaceadaeabcddbebadbbccddaecacdbabdaacccdadbeadeddd"\n', '-1'), ('"ccbaedbbeedbcabdeababdaddadcdbbecbeebaaccacecedddbdeccacdbcacbcadccebbdbecccaccbdaaaaabbeecaaceeeecedeecdccccbdbaeceeccbbceeebebbdbcccccaecebeabaacaadebcdbcaeeeebaccdddbcdddbaddbbacaeeaceabebcbacbbdccbccacacaaaddcedacccadaabedacabdaadcdeeadadcbaedbddacccaebddebaabbbddaecceeedcebebecaebdcdbdaababaaeceaeaadebccaecaaddabdcabaaebadadaedabdcdeebaacdcedccbdacecccbbaadedbbbcdabdaddedeceeeedbaacdddeebcbbdacbcecdcacbddbcabdcaaecbeeabceceeaadbeacdaedcddbaecdbcebbddcdceeecaaeeebddcaceaecbbdbbdcaeaabddabccdedaaebdddbcceabedcccacacecbabdbcabdddbadeceeaeecbbbeecccdeedeadeddbadceeedaccdaccbbabcbedeeaaadabceecdeaacedabeaededebbdeeedebeeddcdbeacecddccbbdadbbdcedceacceaaaebeeeddebcadcebcdeccbaeaacacdceeecdbbbdbdebcaaabadeceeadddbcadadadeeaddbaddacbdadcbbcceecccddcdccdcebdcbecbbccababdbbaaacdbbbdcddbdecaeabecdeeacceedcdeadcedacedbcedeaeacdbeedddeadaaadcbbcaeaaadccdceacacccccaccaebbedadebbdeeeedbbdbcedecdddbabbacacbdcadcbdcbaedcedbeedbeabebecacedaecebbebadbcbadbacabdcdceeecccadcacdbbeaeabccceceaddeeeeadee"\n', '-1')]

def samples():
    return VECTORS[:2]

def cases():
    return [x[0] for x in VECTORS[2:]]

def expected_cases():
    return VECTORS
