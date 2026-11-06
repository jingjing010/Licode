int main(void) {
    int rows;
    int* colSizes;
    int** grid = oj_read_int_matrix(&rows, &colSizes);
    oj_print_int(minPathSum(grid, rows, colSizes));
    return 0;
}
