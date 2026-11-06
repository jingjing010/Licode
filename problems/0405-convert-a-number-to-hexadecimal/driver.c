int main(void) {
    int n = (int)oj_read_ll();
    char *out = toHex(n);
    oj_print_string(out ? out : "");
    free(out);
    return 0;
}
