int main(void) {
    char* s = oj_read_string();
    char* ans = reverseVowels(s);
    oj_print_string(ans ? ans : "");
    return 0;
}
