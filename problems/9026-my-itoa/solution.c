char* my_itoa(int32_t value, char* buf, int base) {
    static const char digits[] = "0123456789ABCDEF";
    char tmp[33];
    int n = 0;
    char* p = buf;
    uint32_t u = (uint32_t)value;
    if (base == 10 && value < 0) {
        *p++ = '-';
        u = 0u - u;
    }
    do {
        tmp[n++] = digits[u % (uint32_t)base];
        u /= (uint32_t)base;
    } while (u != 0);
    while (n > 0) *p++ = tmp[--n];
    *p = '\0';
    return buf;
}
