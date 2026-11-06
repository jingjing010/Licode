char *convertToBase7(int num) {
    long long x = num;
    bool negative = x < 0;
    if (negative)
        x = -x;
    char tmp[32];
    int n = 0;
    do {
        tmp[n++] = '0' + x % 7;
        x /= 7;
    } while (x);
    if (negative)
        tmp[n++] = '-';
    char *out = malloc(n + 1);
    /* 余数按低位到高位产生，需要倒序输出。 */
    for (int i = 0; i < n; ++i)
        out[i] = tmp[n - 1 - i];
    out[n] = 0;
    return out;
}
