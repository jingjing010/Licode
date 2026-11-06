void parse_s16_be(const uint8_t* buf, int len, int32_t* out) {
    for (int i = 0; i < len / 2; i++) {
        uint16_t u = (uint16_t)(((uint16_t)buf[2 * i] << 8) | buf[2 * i + 1]);
        out[i] = (u >= 0x8000u) ? (int32_t)u - 65536 : (int32_t)u;
    }
}
