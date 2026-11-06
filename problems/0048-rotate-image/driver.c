int main(void) {
    int n;
    int* colSizes;
    int** matrix = oj_read_int_matrix(&n, &colSizes);
    rotate(matrix, n, colSizes);
    oj_print_int_matrix(matrix, n, colSizes);
    return 0;
}
