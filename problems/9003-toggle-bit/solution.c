uint32_t toggle_bit(uint32_t reg, int n) {
    return reg ^ (1u << n);
}
