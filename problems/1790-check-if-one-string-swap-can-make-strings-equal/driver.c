int main(void) {
    char *s1 = oj_read_string();
    char *s2 = oj_read_string();
    oj_print_bool(areAlmostEqual(s1, s2));
    free(s1);
    free(s2);
    return 0;
}
