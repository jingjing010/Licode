bool repeatedSubstringPattern(char* s) {
    int n = (int)strlen(s);
    int* nxt = (int*)malloc(sizeof(int) * n);
    nxt[0] = 0;
    for (int i = 1, j = 0; i < n; i++) {
        while (j > 0 && s[i] != s[j]) j = nxt[j - 1];
        if (s[i] == s[j]) j++;
        nxt[i] = j;
    }
    int p = nxt[n - 1];
    free(nxt);
    return p > 0 && n % (n - p) == 0;
}
