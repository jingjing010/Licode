int lowest_set_bit(uint32_t pending) {
    if (pending == 0) {
        return -1;
    }
    int n = 0;
    uint32_t x = pending;
    if ((x & 0x0000FFFFu) == 0) { n += 16; x >>= 16; }
    if ((x & 0x000000FFu) == 0) { n += 8;  x >>= 8; }
    if ((x & 0x0000000Fu) == 0) { n += 4;  x >>= 4; }
    if ((x & 0x00000003u) == 0) { n += 2;  x >>= 2; }
    if ((x & 0x00000001u) == 0) { n += 1; }
    return n;
}
