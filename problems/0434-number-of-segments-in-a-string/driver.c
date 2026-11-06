int main(void) {
    char *s = oj_read_string();
    oj_print_int(countSegments(s));
    free(s);
    return 0;
}
