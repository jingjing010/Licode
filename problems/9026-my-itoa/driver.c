int main(void) {
    int32_t value = (int32_t)oj_read_ll();
    int base = oj_read_int();
    char buf[64];
    memset(buf, 'X', sizeof(buf));
    char* r = my_itoa(value, buf, base);
    if (r != buf) oj_fail("返回值必须是 buf");
    if (memchr(buf, '\0', 34) == NULL) oj_fail("结果没有在 34 字节内以 '\\0' 结尾");
    oj_print_string(buf);
    return 0;
}
