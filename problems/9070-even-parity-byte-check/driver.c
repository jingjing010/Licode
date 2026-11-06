int main(void) {
    int data = (int)oj_read_ll();
    int parity = (int)oj_read_ll();
    oj_print_bool(checkEvenParity(data, parity));
    return 0;
}
