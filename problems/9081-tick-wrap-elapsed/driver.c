int main(void) {
    uint32_t now = (uint32_t)oj_read_ll();
    uint32_t start = (uint32_t)oj_read_ll();
    oj_print_int(elapsedTicks(now, start));
    return 0;
}
