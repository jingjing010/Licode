int main(void) {
    int numRows = oj_read_int();
    int returnSize = 0;
    int* colSizes = NULL;
    int** ans = generate(numRows, &returnSize, &colSizes);
    if (ans == NULL || colSizes == NULL) returnSize = 0;
    oj_print_int_matrix(ans, returnSize, colSizes);
    return 0;
}
