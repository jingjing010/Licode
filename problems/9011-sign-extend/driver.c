int main(void) {
    uint32_t raw = (uint32_t)oj_read_ll();
    int bits = oj_read_int();
    oj_print_int((long long)sign_extend(raw, bits));
    return 0;
}
