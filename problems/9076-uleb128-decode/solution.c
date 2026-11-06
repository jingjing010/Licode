uint32_t uleb128Decode(const uint8_t *data, size_t len) {
    uint32_t value = 0;
    for (size_t i = 0; i < len; ++i)
        value |= (uint32_t)(data[i] & 0x7f) << (7 * i);
    return value;
}
