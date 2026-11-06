int main(void) {
    int digit = (int)oj_read_ll();
    int commonAnode = (int)oj_read_ll();
    oj_print_int(sevenSegment(digit, commonAnode));
    return 0;
}
