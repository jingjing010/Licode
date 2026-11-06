int main(void) {
    int n;
    int* a = oj_read_int_array(&n);
    int k = oj_read_int();
    int x = oj_read_int();
    int returnSize = 0;
    int* ans = findClosestElements(a, n, k, x, &returnSize);
    if (ans == NULL) returnSize = 0;
    oj_print_int_array(ans, returnSize);
    return 0;
}
