char *mergeAlternately(char *word1, char *word2) {
    int n = (int)strlen(word1), m = (int)strlen(word2), k = 0;
    char *out = malloc(n + m + 1);
    for (int i = 0; i < n || i < m; ++i) {
        if (i < n)
            out[k++] = word1[i];
        if (i < m)
            out[k++] = word2[i];
    }
    out[k] = 0;
    return out;
}
