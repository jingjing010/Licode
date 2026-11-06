int main(void) {
    int hourBcd = (int)oj_read_ll();
    int minuteBcd = (int)oj_read_ll();
    int delta = (int)oj_read_ll();
    int returnSize = 0;
    int *out = addBcdMinutes(hourBcd, minuteBcd, delta, &returnSize);
    oj_print_int_array(out, returnSize);
    free(out);
    return 0;
}
