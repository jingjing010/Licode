uint32_t read_be32(const uint8_t* buf, int offset) {
    const uint8_t* p = buf + offset;
    return ((uint32_t)p[0] << 24) | ((uint32_t)p[1] << 16) |
           ((uint32_t)p[2] << 8) | (uint32_t)p[3];
}
