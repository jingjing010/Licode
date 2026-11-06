int main(void) {
    int n;
    int* nums = oj_read_int_array(&n);
    int returnSize = 0;
    int* ans = singleNumber(nums, n, &returnSize);
    if (ans == NULL) returnSize = 0;
    if (returnSize > 1) qsort(ans, returnSize, sizeof(int), oj_cmp_int);
    oj_print_int_array(ans, returnSize);
    return 0;
}
