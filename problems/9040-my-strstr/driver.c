int main(void) {
    char* h = oj_read_string();
    char* nd = oj_read_string();
    int lh = (int)strlen(h);
    char* r = my_strstr(h, nd);
    if (r == NULL) {
        oj_print_int(-1);
    } else if (r < h || r > h + lh) {
        puts("错误：返回的指针不在 haystack 范围内");
    } else {
        oj_print_int((long long)(r - h));
    }
    return 0;
}
