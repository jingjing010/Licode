int main(void) {
    int n;
    int* a = oj_read_int_array(&n);
    int k = oj_read_int();
    int16_t* sig = (int16_t*)malloc(sizeof(int16_t) * (n + 1));
    int16_t* out = (int16_t*)malloc(sizeof(int16_t) * (n + 1));
    for (int i = 0; i < n; i++) sig[i] = (int16_t)a[i];
    medianFilter(sig, (size_t)n, (size_t)k, out);
    int* res = (int*)malloc(sizeof(int) * (n + 1));
    for (int i = 0; i < n; i++) res[i] = out[i];
    oj_print_int_array(res, n);
    return 0;
}
