int main(void) {
    int m;
    int* colSizes;
    int** matrix = oj_read_int_matrix(&m, &colSizes);
    int target = oj_read_int();
    oj_print_bool(searchMatrix(matrix, m, colSizes, target));
    return 0;
}
