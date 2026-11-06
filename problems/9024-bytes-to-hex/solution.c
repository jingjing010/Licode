char* bytes_to_hex(const uint8_t* buf, int len) {
    static const char digits[] = "0123456789ABCDEF";
    char* s = (char*)malloc(len * 2 + 1);
    if (s == NULL) return NULL;
    for (int i = 0; i < len; i++) {
        s[2 * i] = digits[buf[i] >> 4];
        s[2 * i + 1] = digits[buf[i] & 0x0F];
    }
    s[2 * len] = '\0';
    return s;
}
