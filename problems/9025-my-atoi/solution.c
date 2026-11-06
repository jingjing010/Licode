int32_t my_atoi(const char* s) {
    while (*s == ' ') s++;
    int neg = 0;
    if (*s == '+' || *s == '-') {
        neg = (*s == '-');
        s++;
    }
    int64_t v = 0;
    while (*s >= '0' && *s <= '9') {
        v = v * 10 + (*s - '0');
        if (!neg && v > 2147483647LL) return INT32_MAX;
        if (neg && v > 2147483648LL) return INT32_MIN;
        s++;
    }
    return (int32_t)(neg ? -v : v);
}
