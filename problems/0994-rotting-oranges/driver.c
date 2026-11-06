int main(void) {
    int rows;
    int* colSizes = NULL;
    int** grid = oj_read_int_matrix(&rows, &colSizes);
    oj_print_int(orangesRotting(grid, rows, colSizes));
    return 0;
}
