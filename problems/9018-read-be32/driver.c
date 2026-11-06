static uint8_t* drv_read_bytes(int* n) {
    int* a = oj_read_int_array(n);
    uint8_t* b = (uint8_t*)malloc(*n > 0 ? *n : 1);
    for (int i = 0; i < *n; i++) b[i] = (uint8_t)a[i];
    free(a);
    return b;
}

int main(void) {
    int n;
    uint8_t* buf = drv_read_bytes(&n);
    int offset = oj_read_int();
    uint32_t r = read_be32(buf, offset);
    oj_print_int((long long)r);
    return 0;
}
