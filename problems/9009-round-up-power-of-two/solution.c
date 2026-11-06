uint32_t round_up_pow2(uint32_t x) {
    uint32_t v = x - 1u;
    v |= v >> 1;
    v |= v >> 2;
    v |= v >> 4;
    v |= v >> 8;
    v |= v >> 16;
    return v + 1u;
}
