int main(void) {
    char* s = oj_read_string();
    char* t = oj_read_string();
    oj_print_bool(isIsomorphic(s, t));
    return 0;
}
