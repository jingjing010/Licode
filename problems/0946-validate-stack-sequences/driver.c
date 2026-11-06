int main(void) {
    int n, m;
    int* pushed = oj_read_int_array(&n);
    int* popped = oj_read_int_array(&m);
    oj_print_bool(validateStackSequences(pushed, n, popped, m));
    return 0;
}
