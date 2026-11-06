static unsigned char* drv_to_bytes(const int* a, int n) {
    unsigned char* p = (unsigned char*)malloc(n + 1);
    for (int i = 0; i < n; i++) p[i] = (unsigned char)a[i];
    return p;
}

int main(void) {
    int na, nb;
    int* a = oj_read_int_array(&na);
    int* b = oj_read_int_array(&nb);
    int n = oj_read_int();
    if (n < 0 || n > na || n > nb) oj_fail("需要满足 0 <= n <= min(a.length, b.length)");

    unsigned char* pa = drv_to_bytes(a, na);
    unsigned char* pb = drv_to_bytes(b, nb);
    int r = my_memcmp(pa, pb, (size_t)n);
    oj_print_int(r < 0 ? -1 : (r > 0 ? 1 : 0));
    return 0;
}
