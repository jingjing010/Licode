uint8_t swap_nibbles(uint8_t x) {
    return (uint8_t)((x << 4) | (x >> 4));
}
