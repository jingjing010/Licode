int main(void) {
    char* digits = oj_read_string();
    int returnSize = 0;
    char** ans = letterCombinations(digits, &returnSize);
    if (ans == NULL) returnSize = 0;
    oj_sort_string_array(ans, returnSize);
    oj_print_string_array(ans, returnSize);
    return 0;
}
