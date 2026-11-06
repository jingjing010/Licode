int main(void) {
    int rows, cols;
    char** grid = oj_read_char_matrix(&rows, &cols);
    int* colSizes = (int*)malloc(sizeof(int) * (rows > 0 ? rows : 1));
    for (int i = 0; i < rows; i++) colSizes[i] = cols;
    oj_print_int(numIslands(grid, rows, colSizes));
    return 0;
}
