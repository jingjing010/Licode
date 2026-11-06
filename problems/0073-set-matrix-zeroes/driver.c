int main(void) {
    int m;
    int* colSizes;
    int** matrix = oj_read_int_matrix(&m, &colSizes);
    setZeroes(matrix, m, colSizes);
    oj_print_int_matrix(matrix, m, colSizes);
    return 0;
}
