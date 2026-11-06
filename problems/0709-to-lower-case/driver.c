int main(void) {
    char *s = oj_read_string();
    char *out = toLowerCase(s);
    oj_print_string(out ? out : "");
    free(out);
    free(s);
    return 0;
}
