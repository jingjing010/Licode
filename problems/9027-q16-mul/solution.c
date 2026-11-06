int32_t q16_mul(int32_t a, int32_t b) {
    int64_t p = (int64_t)a * (int64_t)b;
    int64_t r = p >> 16;
    if (r > INT32_MAX) return INT32_MAX;
    if (r < INT32_MIN) return INT32_MIN;
    return (int32_t)r;
}
