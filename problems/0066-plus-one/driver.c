int main(void) {
    int n;
    int* digits = oj_read_int_array(&n);
    int returnSize = 0;
    int* res = plusOne(digits, n, &returnSize);
    oj_print_int_array(res, returnSize);
    return 0;
}
