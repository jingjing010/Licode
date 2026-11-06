int main(void) {
    int num = oj_read_int();
    char* ans = intToRoman(num);
    oj_print_string(ans ? ans : "");
    return 0;
}
