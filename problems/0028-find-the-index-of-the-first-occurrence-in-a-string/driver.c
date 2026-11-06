int main(void) {
    char *haystack = oj_read_string();
    char *needle = oj_read_string();
    oj_print_int(strStr(haystack, needle));
    free(haystack);
    free(needle);
    return 0;
}
