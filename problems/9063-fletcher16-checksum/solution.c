uint16_t fletcher16(const uint8_t *data, size_t len) {
    uint32_t a = 0, b = 0;
    for (size_t i = 0; i < len; ++i) {
        a = (a + data[i]) % 255;
        b = (b + a) % 255;
    }
    return (uint16_t)((b << 8) | a);
}
