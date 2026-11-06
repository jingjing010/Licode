int main(void) {
    char *s = oj_read_string();
    char *t = oj_read_string();
    oj_print_bool(isAnagram(s, t));
    free(s);
    free(t);
    return 0;
}
