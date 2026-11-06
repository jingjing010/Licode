int main(void) {
    int n;
    int* bits = oj_read_int_array(&n);
    oj_print_bool(isOneBitCharacter(bits, n));
    return 0;
}
