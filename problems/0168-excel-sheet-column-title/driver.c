int main(void) {
    int n = (int)oj_read_ll();
    char *out = convertToTitle(n);
    oj_print_string(out ? out : "");
    free(out);
    return 0;
}
