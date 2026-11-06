int main(void) {
    int n = oj_read_int();
    int returnSize = 0;
    char** ans = fizzBuzz(n, &returnSize);
    if (ans == NULL) returnSize = 0;
    oj_print_string_array(ans, returnSize);
    return 0;
}
