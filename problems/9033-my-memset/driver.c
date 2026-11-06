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
    int off = oj_read_int();
    int c = oj_read_int();
    int n = oj_read_int();
    if (n < 0 || off < 0 || off + n > len) oj_fail("需要满足 offset + n <= buf.length");

    /* buf 前后各 16 字节哨兵（0xA5），用于检测越界写 */
    unsigned char* raw = (unsigned char*)malloc(len + 32);
    for (int i = 0; i < len + 32; i++) raw[i] = 0xA5;
    unsigned char* buf = raw + 16;
    for (int i = 0; i < len; i++) buf[i] = (unsigned char)a[i];

    void* ret = my_memset(buf + off, c, (size_t)n);

    for (int i = 0; i < 16; i++)
        if (raw[i] != 0xA5 || buf[len + i] != 0xA5) { puts("错误：写到了 buf 之外的内存"); return 0; }
    if (ret != (void*)(buf + off)) { puts("错误：返回值必须是 s"); return 0; }
    drv_print_bytes(buf, len);
    return 0;
}
