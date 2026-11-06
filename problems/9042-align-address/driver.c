int main(void) {
    uintptr_t addr = (uintptr_t)oj_read_ll();
    size_t align = (size_t)oj_read_ll();
    if (align == 0 || (align & (align - 1)) != 0) oj_fail("align 必须是 2 的幂");
    oj_print_int((long long)align_up(addr, align));
    oj_print_int((long long)align_down(addr, align));
    return 0;
}
