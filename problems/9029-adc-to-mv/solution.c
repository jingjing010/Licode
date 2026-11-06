void adc_to_mv(const uint16_t* raw, uint16_t* mv, size_t len, uint8_t bits, uint16_t vref_mv) {
    uint32_t fs = (1u << bits) - 1u;
    for (size_t i = 0; i < len; i++) {
        uint32_t x = (uint32_t)raw[i] * vref_mv;
        mv[i] = (uint16_t)((x + fs / 2u) / fs);
    }
}
