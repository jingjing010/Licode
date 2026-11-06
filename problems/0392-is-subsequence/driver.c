int main(void) {
    char* s = oj_read_string();
    char* t = oj_read_string();
    oj_print_bool(isSubsequence(s, t));
    return 0;
}
