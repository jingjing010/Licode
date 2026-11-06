int main(void) {
    int m;
    int* colSizes;
    int** mat = oj_read_int_matrix(&m, &colSizes);
    int r = oj_read_int();
    int c = oj_read_int();
    int returnSize = 0;
    int* returnColumnSizes = NULL;
    int** ans = matrixReshape(mat, m, colSizes, r, c, &returnSize, &returnColumnSizes);
    if (ans == NULL || returnColumnSizes == NULL) returnSize = 0;
    oj_print_int_matrix(ans, returnSize, returnColumnSizes);
    return 0;
}
