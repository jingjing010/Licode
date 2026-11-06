int main(void) {
    char* s = oj_read_string();
    char* ans = decodeString(s);
    if (ans == NULL) oj_fail("返回值不能是 NULL");
    oj_print_string(ans);
    return 0;
}
