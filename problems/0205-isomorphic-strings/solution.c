bool isIsomorphic(char* s, char* t) {
    unsigned char s2t[256] = {0}, t2s[256] = {0};
    for (int i = 0; s[i] && t[i]; i++) {
        unsigned char a = (unsigned char)s[i], b = (unsigned char)t[i];
        if (s2t[a] == 0 && t2s[b] == 0) {
            s2t[a] = b;
            t2s[b] = a;
        } else if (s2t[a] != b || t2s[b] != a) {
            return false;
        }
    }
    return true;
}
