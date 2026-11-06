int xorChecksum(const uint8_t *data, size_t len) {
    uint8_t value = 0;
    for (size_t i = 0; i < len; ++i)
        value ^= data[i];
    return value;
}
