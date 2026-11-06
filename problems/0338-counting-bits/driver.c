int main(void) {
    int n = oj_read_int();
    int returnSize = 0;
    int* ans = countBits(n, &returnSize);
    if (ans == NULL) returnSize = 0;
    oj_print_int_array(ans, returnSize);
    return 0;
}
