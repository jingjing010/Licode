int main(void) {
    char* d0 = oj_read_string();
    char* src = oj_read_string();
    int ld = (int)strlen(d0), ls = (int)strlen(src);
    int cap = ld + ls + 1;

    /* 缓冲区正好 cap 字节：先放 dst 字符串，剩余填 '#'；后面 16 字节哨兵（0x7F） */
    char* dst = (char*)malloc(cap + 16);
    memset(dst, '#', cap);
    memcpy(dst, d0, ld + 1);
    memset(dst + cap, 0x7F, 16);

    char* ret = my_strcat(dst, src);

    for (int i = 0; i < 16; i++)
        if (dst[cap + i] != 0x7F) { puts("错误：写到了缓冲区之外的内存"); return 0; }
    if (dst[cap - 1] != '\0') { puts("错误：结果没有以 '\\0' 结尾"); return 0; }
    if (ret != dst) { puts("错误：返回值必须是 dst"); return 0; }
    oj_print_string(dst);
    return 0;
}
