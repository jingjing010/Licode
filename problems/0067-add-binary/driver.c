int main(void) {
    char* a = oj_read_string();
    char* b = oj_read_string();
    char* ans = addBinary(a, b);
    oj_print_string(ans ? ans : "");
    return 0;
}
