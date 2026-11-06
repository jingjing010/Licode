char *makeFancyString(char *s) {
    int n = (int)strlen(s), k = 0;
    char *out = malloc(n + 1);
    for (int i = 0; i < n; ++i) {
        if (k >= 2 && out[k - 1] == s[i] && out[k - 2] == s[i])
            continue;
        out[k++] = s[i];
    }
    out[k] = 0;
    return out;
}
