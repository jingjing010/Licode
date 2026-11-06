int main(void) {
    int n = oj_read_int();
    int returnSize = 0;
    char** ans = generateParenthesis(n, &returnSize);
    if (ans == NULL) returnSize = 0;
    oj_sort_string_array(ans, returnSize);
    oj_print_string_array(ans, returnSize);
    return 0;
}
