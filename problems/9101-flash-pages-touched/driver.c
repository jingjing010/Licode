int main(void) {
    uint32_t address = (uint32_t)oj_read_ll();
    uint32_t length = (uint32_t)oj_read_ll();
    int pageSize = (int)oj_read_ll();
    oj_print_int(flashPages(address, length, pageSize));
    return 0;
}
