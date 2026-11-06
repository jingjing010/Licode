# 固定回归向量，预期值由独立 Python 算法预先计算。
VECTORS = [('"A man, a plan, a canal: Panama"\n', 'true'), ('"race a car"\n', 'false'), ('" "\n', 'true'), ('"0P"\n', 'false'), ('"b"\n', 'true'), ('"bB"\n', 'true'), ('"010"\n', 'true'), ('"BaA0,! "\n', 'false'), ('"ABB0,0,0aB! a00A"\n', 'false'), ('"a A ,!a,bA1 ba !b1,b !B,!B!1AAa"\n', 'false'), ('" B0,0,1 0BA!b11 aAb!0bA,bB1BB!1,  bb,,!!B1b!a!, ,0A!1bA 0,,0a, ! 1! !AA !aa01,ba!aAB,b,!A,ba,bAB,0b "\n', 'false'), ('"b,! ba,,!a !A01Aa!b Aa,aBBa1AA  !b10bA1b!b,,a!Aa0bb b0bb1!a,b1, 1b,!a!aaaBA10011110,AbaaA1b aAbBB1b B,, 0,1!b!aA 0ABaB0AAa,1!ABab!1AA0,!1bA,Bb0AAAAB  BbA,11AABA, b0,AB  B,,aB0  AA ,1,1!,!0A0b1 B,,,A!,!0aaba,0b!,001,!a11!0,,0 A00 a0!0abb1!1ba10Baa0Aa1 a! bAb0,0,B0A !0Bb ba10 AaB1 Abaa   BB !!B!,bb !, !AA!B!Bb A1B0aaa1B ,a A,0A,!00001b,!Ba ,,!1Aa1B0!1b , abb,!bb 0AaA1!B bA 0A,,a! 11!, BA  bAb10AaabB,A !bbb1B  ,!Bb!babBb A0ba1bA1aAa! 0100aa!Ba Bb!!B01!,b!10b!bA,Bbaab0,aB AbB aA,A!1!,baA0!1b!1a!A0ba ,!Aa1aBA0a,BB A!0BAbA0,A0bb0B B1Bb  B,11a0,a,aB!, ,, bA,A!b! ab1b AA,,!abA0BaA!!,!b,A AbAbb1aB!AABB11Ab,A baAA!a1ba,BB0a,B1a!1A,0!AAAaa, !ABb1bAaB!AB,1a,a1b,1!!,0!aA1b1ba1, 0b,01aA,00A11!A1,,BBB aB!a1,aB ,AA0BBA!A0!0AB! 1,ba 1a1 A,1A0ABBaabb00b 0,!a1!b !1A, 0!bb0Bb11Bb1!A0BB,,!! ! !,B ABa1ABbb00 0BAb!bAB0!,ba!a,,b1!B!b0,bAbA1Aab 1 !  ,bA,A!!b ,AB,Aba,ABa1b1 !0,!Ba0B1bA,A1B B0Bb  ,10AAAb010! 0b,A aAB0ABb,!0aB,Bab!,,a,, Aa,0 1 ba1 0B0 A10Ba0a,,baBA,0 !aAA1,b0B01!0,Ab ,A0,bbA BB0ab  1 aA,bBa 11!1b"\n', 'false')]

def samples():
    return VECTORS[:2]

def cases():
    return [x[0] for x in VECTORS[2:]]

def expected_cases():
    return VECTORS
