char *toLowerCase(char *s) {
    int n = (int)strlen(s);
    char *out = malloc(n + 1);
    for (int i = 0; i < n; ++i)
        out[i] = (s[i] >= 'A' && s[i] <= 'Z') ? s[i] + ('a' - 'A') : s[i];
    out[n] = 0;
    return out;
}
