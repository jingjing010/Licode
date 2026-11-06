int main(void) {
    uint32_t now = (uint32_t)oj_read_ll();
    uint32_t deadline = (uint32_t)oj_read_ll();
    oj_print_bool(deadlineReached(now, deadline));
    return 0;
}
