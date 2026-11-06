int32_t q16_mul(int32_t a, int32_t b) {
    int64_t p = (int64_t)a * b;
    int64_t q = (p >= 0) ? (p >> 16) : -((-p + 65535) >> 16);
    if (q > INT32_MAX) return INT32_MAX;
    if (q < INT32_MIN) return INT32_MIN;
    return (int32_t)q;
}
