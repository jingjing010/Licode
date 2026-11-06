int main(void) {
    int n;
    int* candidates = oj_read_int_array(&n);
    int target = oj_read_int();
    int returnSize = 0;
    int* colSizes = NULL;
    int** ans = combinationSum(candidates, n, target, &returnSize, &colSizes);
    if (ans == NULL || colSizes == NULL) returnSize = 0;
    oj_sort_int_matrix(ans, returnSize, colSizes, true);
    oj_print_int_matrix(ans, returnSize, colSizes);
    return 0;
}
