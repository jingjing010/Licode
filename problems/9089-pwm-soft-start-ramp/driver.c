int main(void) {
    int initial = (int)oj_read_ll();
    int target = (int)oj_read_ll();
    int step = (int)oj_read_ll();
    int ticks = (int)oj_read_ll();
    oj_print_int(pwmRamp(initial, target, step, ticks));
    return 0;
}
