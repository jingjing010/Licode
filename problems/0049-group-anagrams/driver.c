int main(void) {
    int n;
    char** strs = oj_read_string_array(&n);
    int returnSize = 0;
    int* returnColumnSizes = NULL;
    char*** ans = groupAnagrams(strs, n, &returnSize, &returnColumnSizes);
    if (ans == NULL || returnColumnSizes == NULL) returnSize = 0;
    oj_sort_string_matrix(ans, returnSize, returnColumnSizes, true);
    oj_print_string_matrix(ans, returnSize, returnColumnSizes);
    return 0;
}
