int main(void) {
    char* src = oj_read_string();
    int len = (int)strlen(src);

    /* dst 正好 len + 1 字节，事先填满 '#'；后面 16 字节哨兵（0x7F），用于检测越界写 */
    char* dst = (char*)malloc(len + 1 + 16);
    memset(dst, '#', len + 1);
    memset(dst + len + 1, 0x7F, 16);

    char* ret = my_strcpy(dst, src);

    for (int i = 0; i < 16; i++)
        if (dst[len + 1 + i] != 0x7F) { puts("错误：写到了 dst 之外的内存"); return 0; }
    if (dst[len] != '\0') { puts("错误：没有复制结尾的 '\\0'"); return 0; }
    if (ret != dst) { puts("错误：返回值必须是 dst"); return 0; }
    oj_print_string(dst);
    return 0;
}
