# 固定回归向量，预期值由独立 Python 算法预先计算。
VECTORS = [('"thequickbrownfoxjumpsoverthelazydog"\n', 'true'), ('"leetcode"\n', 'false'), ('"abcdefghijklmnopqrstuvwxyz"\n', 'true'), ('"a"\n', 'false'), ('"p"\n', 'false'), ('"xr"\n', 'false'), ('"xuw"\n', 'false'), ('"uexluix"\n', 'false'), ('"zyfhrzesaqjujeip"\n', 'false'), ('"zxbkqsjdjnybcfcqdbmczpqhjipqfoh"\n', 'false'), ('"tpkzhwicitdptmaqtobwmbkqdehlsgcgtcnwptjqlwgovokwrjdbjslteywzuxhgwvlazgsnkdrlcfmoesybfgiljjricotoslhp"\n', 'true'), ('"hqxrvnngoanzageiayljaxqwnhfdtbhdozyfpsgfqwthfnsklevusafaqcetimxkbqbgvbfbhtarlkjypycirlonsmazzuqoysvkvmlalzxoffnxovrzqzlqkjgdgvyznqfuerzypznmjspotfaqewqrfvygiibsnekyuwibfribqymwuphbnrihikoswwxzcunvnbrhogtloyjqtwocdtwltzhnhhbcayluixijvxczzmyfvloamfzeroyufjidznsdaqpficbjucevtrxvwykengfkmpgmvvfjnpaethdniqgzdxhdqotywbfuiughdrrcozddewuvejxhahihkfooduhqtevwymtmvukrhvgvdnfskuhesvynchgivatycgnimsbfmajfkqkvieqjmnhgxljqqxircmxyylkdycqbellmyuresbvelrxzfhlhczhkbrcimwtrasomoytkwsjygxroytsudxyevtahprzxpzfgrbyiseqjtwzdpcwnvodfrylnvddhldqriclthexdyayxnpdozzrdiymewuqxwqcvobfipizfcvwdhldmfxyfwkmejizxwqpdplwkxxkcokozaxzfazqckdkjekdoztvblrjuexpgmfhqppfskvsdxidfueqyjuzigwsfizuqrhcliucrosqqpncyivsxzbcadtsrgcbksmswaigzmvsufrucwuwjrhemywpvzihufzrjxvrxwzjlceubjlxijvtnvfuowrkhmgjmjedldiqrfyjyloisfwzlxzorpoxulygqjyngjuwiiuaqsxwnflxwqngipulodmfeldewxdfyankzrhozplpdtkroxmazocumrfrsroisoecffvvgfitkhacvfwrucoqwiawvgyyxfxyabuzoqdzwnvawhestbmozrlfnaxqocmjwtrjwdyfmtillisiftazkuzagxhfulbdhsgpovijbkgcmntlewfnwsvtqnmftdpqa"\n', 'true')]

def samples():
    return VECTORS[:2]

def cases():
    return [x[0] for x in VECTORS[2:]]

def expected_cases():
    return VECTORS
