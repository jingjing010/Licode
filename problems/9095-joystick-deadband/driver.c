int main(void) {
    int value = (int)oj_read_ll();
    int threshold = (int)oj_read_ll();
    oj_print_int(applyDeadband(value, threshold));
    return 0;
}
