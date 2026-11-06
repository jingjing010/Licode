int main(void) {
    char *s = oj_read_string();
    oj_print_bool(checkRecord(s));
    free(s);
    return 0;
}
