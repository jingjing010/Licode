bool validateOneWireRom(const uint8_t *rom, size_t len) {
    if (len != 8)
        return false;
    uint8_t crc = 0;
    for (size_t i = 0; i < 7; ++i) {
        crc ^= rom[i];
        for (int b = 0; b < 8; ++b)
            crc = (crc & 1) ? (crc >> 1) ^ 0x8c : crc >> 1;
    }
    return crc == rom[7];
}
