int main(void) {
    int rows;
    int* colSizes;
    int** matrix = oj_read_int_matrix(&rows, &colSizes);
    int target = oj_read_int();
    oj_print_bool(searchMatrix(matrix, rows, colSizes, target));
    return 0;
}
