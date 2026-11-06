int main(void) {
    char *s = oj_read_string();
    oj_print_int(balancedStringSplit(s));
    free(s);
    return 0;
}
