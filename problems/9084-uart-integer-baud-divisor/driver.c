int main(void) {
    int clockHz = (int)oj_read_ll();
    int baud = (int)oj_read_ll();
    oj_print_int(uartDivisor(clockHz, baud));
    return 0;
}
