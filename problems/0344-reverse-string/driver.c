/* 与 oj_print_char_array 相同，但会转义 " 和 \，保证所有可打印字符都能原样输出 */
static void drv_print_chars(const char* s, int n) {
    char one[2] = {0, 0};
    putchar('[');
    for (int i = 0; i < n; i++) {
        if (i) putchar(',');
        one[0] = s[i];
        oj_print_quoted(one);
    }
    printf("]\n");
}

int main(void) {
    int n;
    char* s = oj_read_char_array(&n);
    reverseString(s, n);
    drv_print_chars(s, n);
    return 0;
}
