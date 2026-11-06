int main(void) {
    int n, m;
    int* x = oj_read_int_array(&n);
    int* y = oj_read_int_array(&m);
    if (n != m) oj_fail("a 和 b 的长度必须相同");
    int16_t* a = (int16_t*)malloc(sizeof(int16_t) * (n > 0 ? n : 1));
    int16_t* b = (int16_t*)malloc(sizeof(int16_t) * (n > 0 ? n : 1));
    int16_t* out = (int16_t*)malloc(sizeof(int16_t) * (n > 0 ? n : 1));
    for (int i = 0; i < n; i++) {
        a[i] = (int16_t)x[i];
        b[i] = (int16_t)y[i];
        out[i] = 0;
    }
    sat_add16(a, b, out, (size_t)n);
    for (int i = 0; i < n; i++) x[i] = out[i];
    oj_print_int_array(x, n);
    return 0;
}
