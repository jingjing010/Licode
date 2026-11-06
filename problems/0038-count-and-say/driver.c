int main(void) {
    int n = oj_read_int();
    char* ans = countAndSay(n);
    oj_print_string(ans ? ans : "");
    return 0;
}
