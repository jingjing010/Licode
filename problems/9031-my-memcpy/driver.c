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
    int n = oj_read_int();
    if (n < 0 || n > len) oj_fail("需要满足 0 <= n <= src.length");

    unsigned char* src = (unsigned char*)malloc(len + 1);
    for (int i = 0; i < len; i++) src[i] = (unsigned char)a[i];

    /* dst 前后各 16 字节哨兵（0xAA），用于检测越界写 */
    unsigned char* raw = (unsigned char*)malloc(len + 32);
    memset(raw, 0xAA, len + 32);
    unsigned char* dst = raw + 16;
    memset(dst, 0, len);

    void* ret = my_memcpy(dst, src, (size_t)n);

    for (int i = 0; i < 16; i++)
        if (raw[i] != 0xAA || dst[len + i] != 0xAA) { puts("错误：写到了 dst 之外的内存"); return 0; }
    if (ret != (void*)dst) { puts("错误：返回值必须是 dst"); return 0; }
    drv_print_bytes(dst, len);
    return 0;
}
