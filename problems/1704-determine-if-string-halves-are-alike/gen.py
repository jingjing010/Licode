# 固定回归向量，预期值由独立 Python 算法预先计算。
VECTORS = [('"book"\n', 'true'), ('"textbook"\n', 'false'), ('"Ob"\n', 'false'), ('"azzzEaazIaaObUaI"\n', 'false'), ('"abbzUbOUUOaEOIOOEIaaEIIIIzzbEzbUOIaaOzEOaEIIbzUbzbIUIaOUzabOzzEOUUbzObEaEIIUIzUzOaOEIEbabUEOzUOEEEaI"\n', 'false'), ('"UbaEEaOUIzIUEUzaIUzzUzaEEzOIzOIIIIzEOEzEObEObzOIIIEIIEzIUOEIbbEbUzaOOzUUaEIaaUUbaUOUIzbUUbIbEUbbOEzaaUUzzEIzEOaabEEUObaIIEaUbbbIIEbIUaUzEUUOzIIbUaIOabaIzIIbbbObUbaaIEEaUIEzOEzOzbzzIIaEbOEObbObzOzaazIaaEIUIbEUOIzOzzIOIOIabIOEaUUEUaaEEIazbzOUazEbUaIbIIEIUIEIOzabbazUbOzaIUzUOEOUzEIzUzbaOzEzOEbEEEzUzbabOEEUUEIEOIaIaaIOUEzIIaObaabIUzazzaUzbbabEEIzIOUUUUUOUaaUzazbabzIUUzIIEOzazIEaEEaUzzUUzIIIIaIIIUzzIIIbbzUzEbEzIabUOzIOIIUOEbObOzOUbUaaObzEbzUazaObzOzEbbIOEObIaUEzzUUOOEazIzaazEOaazIOIIbOaOEbEEUOUIaEIazUIaIIzbEbUOOzIaabaaIazzbEUUIEOObbaEzUzOUIaazIOUaaIbOIOOIzUzOzUIaIIbIEEbbabbUUIUEaEEabOIEaEIEEObUIOUzzUbbbEObEIaEIIIEObEOaOzEzOEOOzaOUEUOzEIaEEObzUUEzUbzUEOOazazObzOUbzEIaIOUOaaEUabOEaazaIzIUbOzEEUabzaaObEEOUEOOIEbaIazUUUaEbzbbIIzbUIzEEEOaUbaOEOEazbIzOaIUbazEzOzbOOaEUIIzEaUOUEOUUbaIbUbIOabbUUbabaIIaazIzEzIzzEzazaIUEIOUEaOaazUUUbIOEIIOzOOIzaUEzUOEIOazbzaaUzOUzOEIbazabzaaaUIEaaUabObUOaEzOOIUOOUzUEzEUEEzOzzObzEObbIaOOEbUbIUaOEEUOEEEEOEabOOOOIEbIOOUzaIaOaEOIOaOzzzzOEaUzUUaUUIEIaaOUEzEEbEzEIbbzIbEUIOz"\n', 'false'), ('"ae"\n', 'true'), ('"bc"\n', 'true'), ('"Aa"\n', 'true'), ('"aB"\n', 'false')]

def samples():
    return VECTORS[:2]

def cases():
    return [x[0] for x in VECTORS[2:]]

def expected_cases():
    return VECTORS
