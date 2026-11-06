int main(void) {
    char* s = oj_read_string();
    char* t = oj_read_string();
    char* ans = minWindow(s, t);
    oj_print_string(ans ? ans : "");
    return 0;
}
