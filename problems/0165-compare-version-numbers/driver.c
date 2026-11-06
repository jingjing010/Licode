int main(void) {
    char* v1 = oj_read_string();
    char* v2 = oj_read_string();
    oj_print_int(compareVersion(v1, v2));
    return 0;
}
