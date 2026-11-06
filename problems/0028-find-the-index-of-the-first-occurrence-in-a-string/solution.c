int strStr(char *haystack, char *needle) {
    /* 标准库返回匹配起点，指针相减得到下标。 */
    char *p = strstr(haystack, needle);
    return p ? (int)(p - haystack) : -1;
}
