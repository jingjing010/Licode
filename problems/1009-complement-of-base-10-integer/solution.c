int bitwiseComplement(int n) {
    if (n == 0)
        return 1;
    uint32_t mask = 0, x = (uint32_t)n;
    /* 只翻转有效二进制位，不翻转前导零。 */
    while (x) {
        mask = (mask << 1) | 1u;
        x >>= 1;
    }
    return (int)(mask ^ (uint32_t)n);
}
