int32_t sign_extend(uint32_t raw, int bits) {
    uint32_t m = 1u << (bits - 1);
    return (int32_t)((raw ^ m) - m);
}
