int main(void) {
    int n;
    int* nums = oj_read_int_array(&n);
    int returnSize = 0;
    int* colSizes = NULL;
    int** ans = permute(nums, n, &returnSize, &colSizes);
    if (ans == NULL || colSizes == NULL) returnSize = 0;
    oj_sort_int_matrix(ans, returnSize, colSizes, false);
    oj_print_int_matrix(ans, returnSize, colSizes);
    return 0;
}
