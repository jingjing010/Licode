int main(void) {
    int address = (int)oj_read_ll();
    int read = (int)oj_read_ll();
    oj_print_int(i2cAddressByte(address, read));
    return 0;
}
