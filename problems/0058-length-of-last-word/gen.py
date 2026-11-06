# 固定回归向量，预期值由独立 Python 算法预先计算。
VECTORS = [('"Hello World"\n', '5'), ('"   fly me   to   the moon  "\n', '4'), ('"a"\n', '1'), ('"a  "\n', '1'), ('"e"\n', '1'), ('"bb"\n', '2'), ('"bab"\n', '3'), ('"ddcccde"\n', '7'), ('"dceaadbdadedcaab"\n', '16'), ('"cabccbeebabbdbbbbaccadeececedbc"\n', '31'), ('"cbdbebdeeabadccddcdbabaebacaabeaaadaecdecceacabbbbcdadbbebaabeacdcdacaededddacaebdbeabdaabaedbcedade"\n', '100'), ('"abcaecadadeaebdcaccbbaabcddcbbdceccadecabcbaecebebdbbcbbadeedebdbabebeceabbdeecdedddacaeacaadccbdbcebdcdbebbbdeadcbadeeabdbedcdcceabaddcacaebbeccbdbcdbcbabdadddcbcacaaebbadebbdcadcccbcbdcedabedbcaadedabaeadbedadeacabadaaecccbbacaddbeacbcaaeaacaadbcdcdacedededddceebdddbdcbbbdebbebacbbedadedddbbbdcbebdcdcbcadbbdcbdeaddcebdacceaddccedabcedcdbdccededceeccdcadecbcecdceaceacaacadaeaebdceebcaddbeaacddbeadadedaccabedcbbbdecdecaaceeecbcbdebdecbacadbdcaededccbcddaaabcebaeebcdcbaecbdaccddcbddebebecedbeedddcedcbedbacaeecbeaccecaebdbaaaaedcdedbadaaabedbaaaadaadbddadbdbbccacdacadedbecedeecbdcedaebeaaeebcededdbaaebdbadeedbeeacbeccdcecaeeedcadaebdbeacbbeeaecbdeabcbccdeccecdadbdbdbbcaabdbbbbbeddeddbbcebedcaeccbeaebdaaddecccedbbbaabebaaededeedebcabecdaddeedccaaeacdabcdecaceeedaaebecddbbcdeaecbaebeabbbaddedccabedebcccceedbdaeccdbabbcbdbddaabbbaebedebddedeadecbbcedbebedddbdadeccbdebdeebbccbbcddeddbcbbcbbaeacdcdeadcdcabbccaaaddedadbbadbcedcdbeaeebdbabaaedaacdcacbdcebddedebdbcbbadbacbedcdcccdebeadbacdcaaeda"\n', '1000')]

def samples():
    return VECTORS[:2]

def cases():
    return [x[0] for x in VECTORS[2:]]

def expected_cases():
    return VECTORS
