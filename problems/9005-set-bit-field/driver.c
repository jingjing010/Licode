int main(void) {
    uint32_t reg = (uint32_t)oj_read_ll();
    int pos = oj_read_int();
    int width = oj_read_int();
    uint32_t val = (uint32_t)oj_read_ll();
    oj_print_int((long long)set_bit_field(reg, pos, width, val));
    return 0;
}
