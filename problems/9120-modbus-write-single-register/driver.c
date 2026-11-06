int main(void) {
    int address = (int)oj_read_ll();
    int reg = (int)oj_read_ll();
    int value = (int)oj_read_ll();
    int returnSize = 0;
    int *out = modbusWriteSingle(address, reg, value, &returnSize);
    oj_print_int_array(out, returnSize);
    free(out);
    return 0;
}
