int main(void) {
    int32_t value = (int32_t)oj_read_ll();
    int base = oj_read_int();
    char buf[64];
    memset(buf, '#', sizeof(buf));
    buf[63] = '\0';
    char* r = my_itoa(value, buf, base);
    if (r != buf) oj_fail("返回值必须是 buf");
    oj_print_string(buf);
    return 0;
}
