char *replaceDigits(char *s) {
    int n = (int)strlen(s);
    char *out = malloc(n + 1);
    memcpy(out, s, n + 1);
    for (int i = 1; i < n; i += 2)
        out[i] = out[i - 1] + (s[i] - '0');
    return out;
}
