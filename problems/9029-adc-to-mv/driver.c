int main(void) {
    int n;
    int* a = oj_read_int_array(&n);
    uint8_t bits = (uint8_t)oj_read_int();
    uint16_t vref = (uint16_t)oj_read_int();
    uint16_t* raw = (uint16_t*)malloc(sizeof(uint16_t) * (n > 0 ? n : 1));
    uint16_t* mv = (uint16_t*)malloc(sizeof(uint16_t) * (n > 0 ? n : 1));
    for (int i = 0; i < n; i++) {
        raw[i] = (uint16_t)a[i];
        mv[i] = 0;
    }
    adc_to_mv(raw, mv, (size_t)n, bits, vref);
    for (int i = 0; i < n; i++) a[i] = mv[i];
    oj_print_int_array(a, n);
    return 0;
}
