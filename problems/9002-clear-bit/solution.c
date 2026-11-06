uint32_t clear_bit(uint32_t reg, int n) {
    return reg & ~(1u << n);
}
