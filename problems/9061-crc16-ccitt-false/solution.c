uint16_t crc16Ccitt(const uint8_t *data, size_t len) {
    uint16_t crc = 0xffff;
    for (size_t i = 0; i < len; ++i) {
        crc ^= (uint16_t)data[i] << 8;
        /* 非反射算法：从最高位移出，生成多项式为0x1021。 */
        for (int bit = 0; bit < 8; ++bit)
            crc = (uint16_t)((crc & 0x8000) ? (crc << 1) ^ 0x1021 : crc << 1);
    }
    return crc;
}
