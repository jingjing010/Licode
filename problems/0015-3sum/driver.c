int main(void) {
    int n;
    int* nums = oj_read_int_array(&n);
    int returnSize = 0;
    int* returnColumnSizes = NULL;
    int** ans = threeSum(nums, n, &returnSize, &returnColumnSizes);
    if (ans == NULL || returnColumnSizes == NULL) returnSize = 0;
    oj_sort_int_matrix(ans, returnSize, returnColumnSizes, true);
    oj_print_int_matrix(ans, returnSize, returnColumnSizes);
    return 0;
}
