# 固定回归向量，预期值由独立 Python 算法预先计算。
VECTORS = [('"ab-cd"\n', '"dc-ba"'), ('"a-bC-dEf-ghIj"\n', '"j-Ih-gfE-dCba"'), ('"Test1ng-Leet=code-Q!"\n', '"Qedo1ct-eeLg=ntse-T!"'), ('"!"\n', '"!"'), ('"A"\n', '"A"'), ('"aA"\n', '"Aa"'), ('"!!0"\n', '"!!0"'), ('"-A!=-A!"\n', '"-A!=-A!"'), ('"--aAzAZzZ0aZ0A0="\n', '"--AZaZzZA0zA0a0="'), ('"A!zZZ--a!ZZ=A00=aZ=0=Za0-A0-!0="\n', '"A!aZZ--a!AZ=Z00=aZ=0=Zz0-A0-!0="'), ('"Z!=-=Z0z=aA00Az0azz!0!--za!A0Aa!AZa0Z!!Aa-!=0=!ZA00!aaaz-=!-=-0=z0Z!a--=-ZzA!z==!Aa=-0Aaz!-z=!a=A0!0"\n', '"A!=-=a0z=za00Aa0AzA!0!--zZ!a0Zz!zaa0a!!AZ-!=0=!aA00!ZaZA-=!-=-0=a0A!A--=-azz!z==!az=-0AAa!-z=!Z=Z0!0"')]

def samples():
    return VECTORS[:2]

def cases():
    return [x[0] for x in VECTORS[2:]]

def expected_cases():
    return VECTORS
