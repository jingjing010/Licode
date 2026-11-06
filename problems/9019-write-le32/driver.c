int main(void) {
    int n;
    int* a = oj_read_int_array(&n);
    int offset = oj_read_int();
    uint32_t value = (uint32_t)oj_read_ll();
    uint8_t* buf = (uint8_t*)malloc(n > 0 ? n : 1);
    for (int i = 0; i < n; i++) buf[i] = (uint8_t)a[i];
    write_le32(buf, offset, value);
    for (int i = 0; i < n; i++) a[i] = buf[i];
    oj_print_int_array(a, n);
    return 0;
}
