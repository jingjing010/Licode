int main(void) {
    uint8_t data = (uint8_t)oj_read_int();
    int odd = oj_read_int();
    oj_print_int((long long)parity_bit(data, odd));
    return 0;
}
