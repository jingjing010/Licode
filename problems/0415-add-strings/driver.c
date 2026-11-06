int main(void) {
    char* num1 = oj_read_string();
    char* num2 = oj_read_string();
    char* ans = addStrings(num1, num2);
    oj_print_string(ans ? ans : "");
    return 0;
}
