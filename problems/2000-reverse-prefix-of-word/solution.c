char *reversePrefix(char *word, char ch) {
    int n = (int)strlen(word), end = -1;
    char *out = malloc(n + 1);
    memcpy(out, word, n + 1);
    for (int i = 0; i < n; ++i)
        if (word[i] == ch) {
            end = i;
            break;
        }
    for (int l = 0, r = end; l < r; ++l, --r) {
        char c = out[l];
        out[l] = out[r];
        out[r] = c;
    }
    return out;
}
