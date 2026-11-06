int main(void) {
    int n;
    int* a = oj_read_int_array(&n);
    for (int i = 0; i < n; i++) a[i] = (int)bin_to_bcd((uint8_t)a[i]);
    oj_print_int_array(a, n);
    return 0;
}
