int main(void) {
    char* hex = oj_read_string();
    int cap = (int)strlen(hex) / 2;
    uint8_t* out = (uint8_t*)malloc(cap > 0 ? cap : 1);
    for (int i = 0; i < cap; i++) out[i] = 0xA5;
    int r = hex_to_bytes(hex, out);
    oj_print_int(r);
    if (r >= 0) {
        if (r > cap) oj_fail("返回值超过 strlen(hex) / 2");
        int* a = (int*)malloc(sizeof(int) * (r > 0 ? r : 1));
        for (int i = 0; i < r; i++) a[i] = out[i];
        oj_print_int_array(a, r);
    }
    return 0;
}
