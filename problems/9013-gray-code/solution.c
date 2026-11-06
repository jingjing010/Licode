uint32_t gray_to_binary(uint32_t gray) {
    uint32_t b = gray;
    b ^= b >> 16;
    b ^= b >> 8;
    b ^= b >> 4;
    b ^= b >> 2;
    b ^= b >> 1;
    return b;
}
