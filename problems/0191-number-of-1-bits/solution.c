int hammingWeight(uint32_t n) {
    n = n - ((n >> 1) & 0x55555555u);
    n = (n & 0x33333333u) + ((n >> 2) & 0x33333333u);
    n = (n + (n >> 4)) & 0x0F0F0F0Fu;
    return (int)((n * 0x01010101u) >> 24);
}
