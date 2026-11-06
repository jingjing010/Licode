int main(void) {
    char* s = oj_read_string();
    int returnSize = 0;
    int* colSizes = NULL;
    char*** ans = partition(s, &returnSize, &colSizes);
    if (ans == NULL || colSizes == NULL) returnSize = 0;
    oj_sort_string_matrix(ans, returnSize, colSizes, false);
    oj_print_string_matrix(ans, returnSize, colSizes);
    return 0;
}
