int main(void) {
    int rows;
    int* colSizes;
    int** matrix = oj_read_int_matrix(&rows, &colSizes);
    int returnSize = 0;
    int* returnColumnSizes = NULL;
    int** ans = transpose(matrix, rows, colSizes, &returnSize, &returnColumnSizes);
    if (ans == NULL || returnColumnSizes == NULL) returnSize = 0;
    oj_print_int_matrix(ans, returnSize, returnColumnSizes);
    return 0;
}
