uint16_t swap16(uint16_t x) {
    return (uint16_t)(((x & 0x00FFu) << 8) | ((x >> 8) & 0x00FFu));
}
