int main(void) {
    uint32_t x = (uint32_t)oj_read_ll();
    oj_print_int((long long)round_up_pow2(x));
    return 0;
}
