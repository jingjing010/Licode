char* intToRoman(int num) {
    static const int vals[13] = {1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1};
    static const char* syms[13] = {"M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"};
    char* res = (char*)malloc(16);
    int len = 0;
    for (int i = 0; i < 13; i++) {
        while (num >= vals[i]) {
            for (const char* p = syms[i]; *p; p++) res[len++] = *p;
            num -= vals[i];
        }
    }
    res[len] = '\0';
    return res;
}
