char *freqAlphabets(char *s) {
    int n = (int)strlen(s), k = 0;
    char *out = malloc(n + 1);
    for (int i = 0; i < n;) {
        int value;
        if (i + 2 < n && s[i + 2] == '#') {
            value = (s[i] - '0') * 10 + s[i + 1] - '0';
            i += 3;
        } else {
            value = s[i] - '0';
            ++i;
        }
        out[k++] = 'a' + value - 1;
    }
    out[k] = 0;
    return out;
}
