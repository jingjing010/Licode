int main(void) {
    char* s1 = oj_read_string();
    char* s2 = oj_read_string();
    int r = my_strcmp(s1, s2);
    oj_print_int(r < 0 ? -1 : (r > 0 ? 1 : 0));
    return 0;
}
