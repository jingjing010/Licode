int main(void) {
    long long a = oj_read_ll();
    long long al = oj_read_ll();
    if (a < 0 || a > 0xFFFFFFFFLL) oj_fail("addr 超出范围");
    if (al < 1 || al > 4096 || (al & (al - 1)) != 0) oj_fail("align 必须是 1 ~ 4096 之间的 2 的幂");
    uintptr_t addr = (uintptr_t)a;
    size_t align = (size_t)al;
    oj_print_bool(is_aligned(addr, align));
    oj_print_int((long long)align_padding(addr, align));
    return 0;
}
