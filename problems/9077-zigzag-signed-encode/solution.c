uint32_t zigzagEncode(int32_t value) {
    /* 先转无符号再移位，避免对负数左移。 */
    return ((uint32_t)value << 1) ^ (value < 0 ? UINT32_MAX : 0u);
}
