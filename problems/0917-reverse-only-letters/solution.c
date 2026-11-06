char *reverseOnlyLetters(char *s) {
    int n = (int)strlen(s), l = 0, r = n - 1;
    char *out = malloc(n + 1);
    memcpy(out, s, n + 1);
    while (l < r) {
        while (l < r && !isalpha((unsigned char)out[l]))
            ++l;
        while (l < r && !isalpha((unsigned char)out[r]))
            --r;
        char t = out[l];
        out[l++] = out[r];
        out[r--] = t;
    }
    return out;
}
