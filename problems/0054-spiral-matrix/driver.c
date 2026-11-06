int main(void) {
    int m;
    int* colSizes;
    int** matrix = oj_read_int_matrix(&m, &colSizes);
    int returnSize = 0;
    int* ans = spiralOrder(matrix, m, colSizes, &returnSize);
    if (ans == NULL) returnSize = 0;
    oj_print_int_array(ans, returnSize);
    return 0;
}
