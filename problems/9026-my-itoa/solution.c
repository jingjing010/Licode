char* my_itoa(int32_t value, char* buf, int base) {
    static const char digits[] = "0123456789ABCDEF";
    uint32_t u = (uint32_t)value;
    int pos = 0;
    if (base == 10 && value < 0) {
        buf[pos++] = '-';
        u = 0u - u;
    }
    int start = pos;
    do {
        buf[pos++] = digits[u % (uint32_t)base];
        u /= (uint32_t)base;
    } while (u != 0);
    buf[pos] = '\0';
    for (int i = start, j = pos - 1; i < j; i++, j--) {
        char t = buf[i];
        buf[i] = buf[j];
        buf[j] = t;
    }
    return buf;
}
