int main(void) {
    uint32_t reg = (uint32_t)oj_read_ll();
    int n = oj_read_int();
    oj_print_int((long long)toggle_bit(reg, n));
    return 0;
}
