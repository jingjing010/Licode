int main(void) {
    uint32_t elapsed = (uint32_t)oj_read_ll();
    uint32_t minimum = (uint32_t)oj_read_ll();
    uint32_t maximum = (uint32_t)oj_read_ll();
    oj_print_bool(watchdogCanFeed(elapsed, minimum, maximum));
    return 0;
}
