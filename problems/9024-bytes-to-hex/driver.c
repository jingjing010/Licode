int main(void) {
    int n;
    int* a = oj_read_int_array(&n);
    uint8_t* buf = (uint8_t*)malloc(n > 0 ? n : 1);
    for (int i = 0; i < n; i++) buf[i] = (uint8_t)a[i];
    char* s = bytes_to_hex(buf, n);
    if (s == NULL) oj_fail("返回了 NULL");
    oj_print_string(s);
    free(s);
    return 0;
}
