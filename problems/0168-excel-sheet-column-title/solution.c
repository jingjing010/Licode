char *convertToTitle(int columnNumber) {
    char tmp[16];
    int n = 0;
    /* 列号从1开始，每次先减1再做26进制转换。 */
    while (columnNumber) {
        --columnNumber;
        tmp[n++] = 'A' + columnNumber % 26;
        columnNumber /= 26;
    }
    char *out = malloc(n + 1);
    for (int i = 0; i < n; ++i)
        out[i] = tmp[n - 1 - i];
    out[n] = '\0';
    return out;
}
