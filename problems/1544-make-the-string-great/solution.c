char *makeGood(char *s) {
    int n = (int)strlen(s), top = 0;
    char *out = malloc(n + 1);
    /* 栈顶与当前字符是同字母不同大小写时互相消去。 */
    for (int i = 0; i < n; ++i) {
        if (top > 0 && abs(out[top - 1] - s[i]) == 32)
            --top;
        else
            out[top++] = s[i];
    }
    out[top] = 0;
    return out;
}
