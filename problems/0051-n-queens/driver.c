int main(void) {
    int n = oj_read_int();
    int returnSize = 0;
    int* colSizes = NULL;
    char*** ans = solveNQueens(n, &returnSize, &colSizes);
    if (ans == NULL || colSizes == NULL) returnSize = 0;
    oj_sort_string_matrix(ans, returnSize, colSizes, false);
    oj_print_string_matrix(ans, returnSize, colSizes);
    return 0;
}
