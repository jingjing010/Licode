int main(void) {
    int n;
    int* colSizes;
    int** intervals = oj_read_int_matrix(&n, &colSizes);
    int returnSize = 0;
    int* returnColumnSizes = NULL;
    int** ans = merge(intervals, n, colSizes, &returnSize, &returnColumnSizes);
    if (ans == NULL || returnColumnSizes == NULL) returnSize = 0;
    oj_sort_int_matrix(ans, returnSize, returnColumnSizes, false);
    oj_print_int_matrix(ans, returnSize, returnColumnSizes);
    return 0;
}
