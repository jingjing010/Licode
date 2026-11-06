int main(void) {
    int n;
    int* a = oj_read_int_array(&n);
    uint8_t* buf = (uint8_t*)malloc(n > 0 ? n : 1);
    for (int i = 0; i < n; i++) buf[i] = (uint8_t)a[i];
    oj_print_int((long long)checksum8(buf, (size_t)n));
    return 0;
}
