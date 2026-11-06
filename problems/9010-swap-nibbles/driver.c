int main(void) {
    uint8_t x = (uint8_t)oj_read_int();
    oj_print_int((long long)swap_nibbles(x));
    return 0;
}
