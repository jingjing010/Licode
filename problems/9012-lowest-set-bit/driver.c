int main(void) {
    uint32_t pending = (uint32_t)oj_read_ll();
    oj_print_int(lowest_set_bit(pending));
    return 0;
}
