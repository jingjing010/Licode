uint32_t get_bit_field(uint32_t reg, int pos, int width) {
    uint32_t mask = (width >= 32) ? 0xFFFFFFFFu : ((1u << width) - 1u);
    return (reg >> pos) & mask;
}
