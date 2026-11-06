static void drv_print_buf(const char* p, int n) {
    putchar('"');
    for (int i = 0; i < n; i++) {
        if (p[i] == '\0') printf("\\0");
        else putchar(p[i]);
    }
    printf("\"\n");
}

int main(void) {
    char* src = oj_read_string();
    int n = oj_read_int();
    if (n < 0) oj_fail("n 不能为负数");

    /* dst 共 n + 3 字节，全部填 '*'；后面 16 字节哨兵（0x7F），用于检测越界写 */
    int cap = n + 3;
    char* dst = (char*)malloc(cap + 16);
    memset(dst, '*', cap);
    memset(dst + cap, 0x7F, 16);

    char* ret = my_strncpy(dst, src, (size_t)n);

    for (int i = 0; i < 16; i++)
        if (dst[cap + i] != 0x7F) { puts("错误：写到了缓冲区之外的内存"); return 0; }
    if (ret != dst) { puts("错误：返回值必须是 dst"); return 0; }
    drv_print_buf(dst, cap);
    return 0;
}
