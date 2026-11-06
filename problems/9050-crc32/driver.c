int main(void) {
    int n;
    int* a = oj_read_int_array(&n);
    uint8_t* buf = (uint8_t*)malloc(n + 1);
    for (int i = 0; i < n; i++) buf[i] = (uint8_t)a[i];
    uint32_t crc = crc32(buf, (size_t)n);
    printf("%u\n", (unsigned)crc);
    free(buf);
    return 0;
}
