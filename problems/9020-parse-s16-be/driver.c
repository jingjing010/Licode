int main(void) {
    int n;
    int* a = oj_read_int_array(&n);
    uint8_t* buf = (uint8_t*)malloc(n > 0 ? n : 1);
    for (int i = 0; i < n; i++) buf[i] = (uint8_t)a[i];
    int m = n / 2;
    int32_t* out = (int32_t*)malloc(sizeof(int32_t) * (m > 0 ? m : 1));
    for (int i = 0; i < m; i++) out[i] = 0x5A5A5A5A;
    parse_s16_be(buf, n, out);
    int* res = (int*)malloc(sizeof(int) * (m > 0 ? m : 1));
    for (int i = 0; i < m; i++) res[i] = (int)out[i];
    oj_print_int_array(res, m);
    return 0;
}
