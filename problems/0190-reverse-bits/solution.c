uint32_t reverseBits(uint32_t n) {
    n = ((n >> 1) & 0x55555555u) | ((n & 0x55555555u) << 1);
    n = ((n >> 2) & 0x33333333u) | ((n & 0x33333333u) << 2);
    n = ((n >> 4) & 0x0F0F0F0Fu) | ((n & 0x0F0F0F0Fu) << 4);
    n = ((n >> 8) & 0x00FF00FFu) | ((n & 0x00FF00FFu) << 8);
    return (n >> 16) | (n << 16);
}
