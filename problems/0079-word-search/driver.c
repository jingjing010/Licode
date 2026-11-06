int main(void) {
    int rows, cols;
    char** board = oj_read_char_matrix(&rows, &cols);
    char* word = oj_read_string();
    int* colSizes = (int*)malloc(sizeof(int) * (rows > 0 ? rows : 1));
    for (int i = 0; i < rows; i++) colSizes[i] = cols;
    oj_print_bool(exist(board, rows, colSizes, word));
    return 0;
}
