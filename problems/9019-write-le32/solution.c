void write_le32(uint8_t* buf, int offset, uint32_t value) {
    buf[offset + 0] = (uint8_t)(value & 0xFFu);
    buf[offset + 1] = (uint8_t)((value >> 8) & 0xFFu);
    buf[offset + 2] = (uint8_t)((value >> 16) & 0xFFu);
    buf[offset + 3] = (uint8_t)((value >> 24) & 0xFFu);
}
