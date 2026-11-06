int main(void) {
    char* s = oj_read_string();
    int m;
    char** dict = oj_read_string_array(&m);
    oj_print_bool(wordBreak(s, dict, m));
    return 0;
}
