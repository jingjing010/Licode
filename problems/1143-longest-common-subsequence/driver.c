int main(void) {
    char* text1 = oj_read_string();
    char* text2 = oj_read_string();
    oj_print_int(longestCommonSubsequence(text1, text2));
    return 0;
}
