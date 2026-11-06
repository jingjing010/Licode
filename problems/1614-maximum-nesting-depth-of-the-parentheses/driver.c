int main(void) {
    char *s = oj_read_string();
    oj_print_int(maxDepth(s));
    free(s);
    return 0;
}
