char *toHex(int num) {
    uint32_t x = (uint32_t)num;
    char tmp[8];
    int n = 0;
    /* 负数按32位补码解释，每次取最低4位。 */
    do {
        tmp[n++] = "0123456789abcdef"[x & 15];
        x >>= 4;
    } while (x);
    char *out = malloc(n + 1);
    for (int i = 0; i < n; ++i)
        out[i] = tmp[n - 1 - i];
    out[n] = 0;
    return out;
}
