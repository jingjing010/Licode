char findTheDifference(char* s, char* t) {
    char x = 0;
    for (; *s; s++) x ^= *s;
    for (; *t; t++) x ^= *t;
    return x;
}
