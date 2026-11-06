uint32_t set_bit_field(uint32_t reg, int pos, int width, uint32_t val) {
    uint32_t mask = (width >= 32) ? 0xFFFFFFFFu : ((1u << width) - 1u);
    reg &= ~(mask << pos);
    reg |= (val & mask) << pos;
    return reg;
}
