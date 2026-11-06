uint8_t parity_bit(uint8_t data, int odd) {
    uint8_t x = data;
    x ^= x >> 4;
    x ^= x >> 2;
    x ^= x >> 1;
    return (uint8_t)((x & 1u) ^ (odd ? 1u : 0u));
}
