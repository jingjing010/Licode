int main(void) {
    uint32_t reg = (uint32_t)oj_read_ll();
    int pos = oj_read_int();
    int width = oj_read_int();
    oj_print_int((long long)get_bit_field(reg, pos, width));
    return 0;
}
