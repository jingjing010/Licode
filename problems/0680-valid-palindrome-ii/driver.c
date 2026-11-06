int main(void) {
    char *s = oj_read_string();
    oj_print_bool(validPalindrome(s));
    free(s);
    return 0;
}
