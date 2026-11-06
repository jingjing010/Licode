static void drv_print_bytes(const unsigned char* p, int n) {
    putchar('[');
    for (int i = 0; i < n; i++) {
        if (i) putchar(',');
        printf("%d", (int)p[i]);
    }
    printf("]\n");
}

int main(void) {
    int len;
    int* a = oj_read_int_array(&len);
    int doff = oj_read_int();
    int soff = oj_read_int();
    int n = oj_read_int();
    if (n < 0 || doff < 0 || soff < 0 || doff + n > len || soff + n > len)
        oj_fail("需要满足 dstOffset + n <= buf.length 且 srcOffset + n <= buf.length");

    /* buf 前后各 16 字节哨兵（0xAA），用于检测越界写 */
    unsigned char* raw = (unsigned char*)malloc(len + 32);
    memset(raw, 0xAA, len + 32);
    unsigned char* buf = raw + 16;
    for (int i = 0; i < len; i++) buf[i] = (unsigned char)a[i];

    void* ret = my_memmove(buf + doff, buf + soff, (size_t)n);

    for (int i = 0; i < 16; i++)
        if (raw[i] != 0xAA || buf[len + i] != 0xAA) { puts("错误：写到了 buf 之外的内存"); return 0; }
    if (ret != (void*)(buf + doff)) { puts("错误：返回值必须是 dst"); return 0; }
    drv_print_bytes(buf, len);
    return 0;
}
