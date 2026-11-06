char *removeOuterParentheses(char *s) {
    char *out = malloc(strlen(s) + 1);
    int depth = 0, k = 0;
    for (int i = 0; s[i]; ++i) {
        if (s[i] == '(') {
            if (depth > 0)
                out[k++] = s[i];
            ++depth;
        } else {
            --depth;
            if (depth > 0)
                out[k++] = s[i];
        }
    }
    out[k] = 0;
    return out;
}
